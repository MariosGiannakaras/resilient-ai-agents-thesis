"""Deterministic, presentation-only T-613 assets from the finalized T-612 package."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from resilient_agents.evidence_v2 import validate_protocol_v21_final_freeze
from resilient_agents.evidence_v2.final_analysis import verify_protocol_v21_t612

PACKAGE_RELATIVE = Path("results/thesis-assets/protocol-v2.1-final")
STUDY_EXPORT_RELATIVE = Path(
    "results/studies/protocol-v2.1-final--t610-recovery-01/derived/export"
)
ANALYSIS_MANIFEST_RELATIVE = Path("results/analysis/protocol-v2.1-final/analysis-manifest.json")
DIAGNOSTICS_RELATIVE = Path("results/analysis/protocol-v2.1-final/diagnostics.json")
FREEZE_MANIFEST_RELATIVE = Path("results/final-evidence/protocol-v2.1-final/freeze-manifest.json")
EXPECTED_FREEZE_SHA = "20a88bf9eee2ba8c4f60064634004f3746a594460f91fcd2491beae5cb498858"
EXPECTED_INVENTORY_SHA = "0c2b352b88045951d32e58ee3479656dce00e35d55899bcdea65dc07604d8045"
EXPECTED_ANALYSIS_SHA = "dd467d1f282b183ccf767084639b5ad38cc02caa5e3b6ce521128d177bb3ee62"
GENERATOR_VERSION = "t613-assets-v1"
METHODS = ["q_learning", "sarsa", "dyna_q_plus", "dqn", "ppo"]
METHOD_LABELS = {
    "q_learning": "Q-Learning", "sarsa": "SARSA", "dyna_q_plus": "Dyna-Q+",
    "dqn": "DQN", "ppo": "PPO",
}
CONDITIONS = [
    "action-remap-cycle-clockwise", "action-remap-swap-right-down",
    "action-failure-0.15", "observation-corruption-0.05",
]
CONDITION_LABELS = {
    "action-remap-cycle-clockwise": "Action remap: cycle",
    "action-remap-swap-right-down": "Action remap: swap",
    "action-failure-0.15": "Action failure 0.15",
    "observation-corruption-0.05": "Observation corruption 0.05",
}
COLORS = {
    "q_learning": "#0072B2", "sarsa": "#E69F00", "dyna_q_plus": "#009E73",
    "dqn": "#CC79A7", "ppo": "#D55E00",
}
MARKERS = {"q_learning": "o", "sarsa": "s", "dyna_q_plus": "^", "dqn": "D", "ppo": "P"}
LINESTYLES = {"q_learning": "-", "sarsa": "--", "dyna_q_plus": "-.", "dqn": ":", "ppo": (0, (5, 2))}
FIGURE_METADATA = {"Creator": GENERATOR_VERSION, "Date": None}


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical_json(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def _configure(font_size: float = 9.0) -> None:
    matplotlib.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": font_size,
        "axes.titlesize": font_size + 1, "axes.labelsize": font_size,
        "legend.fontsize": font_size - 1, "xtick.labelsize": font_size - 1,
        "ytick.labelsize": font_size - 1, "axes.spines.top": False,
        "axes.spines.right": False, "axes.grid": True, "grid.color": "#d9d9d9",
        "grid.linewidth": 0.55, "grid.alpha": 0.8, "figure.dpi": 110,
        "savefig.dpi": 300, "svg.hashsalt": "protocol-v2.1-final-t613",
        "pdf.compression": 9,
    })


def _legend(ax: plt.Axes, *, ncol: int = 3) -> None:
    handles = [Line2D([0], [0], color=COLORS[m], marker=MARKERS[m], linestyle=LINESTYLES[m], label=METHOD_LABELS[m]) for m in METHODS]
    ax.legend(handles=handles, ncol=ncol, frameon=False)


def _finish(fig: plt.Figure, base: Path) -> list[Path]:
    fig.align_labels()
    if not fig.get_constrained_layout():
        fig.tight_layout(rect=(0, 0, 1, 0.98))
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight", metadata=FIGURE_METADATA)
    svg_path = base.with_suffix(".svg")
    svg_path.write_bytes(svg_path.read_bytes().replace(b"\r\n", b"\n"))
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight", metadata={"Creator": GENERATOR_VERSION, "Producer": GENERATOR_VERSION, "CreationDate": None, "ModDate": None})
    fig.savefig(base.with_suffix(".png"), bbox_inches="tight", dpi=300, metadata={"Software": GENERATOR_VERSION})
    plt.close(fig)
    return [base.with_suffix(s) for s in (".svg", ".pdf", ".png")]


def _method_order(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result["method_id"] = pd.Categorical(result["method_id"], METHODS, ordered=True)
    return result.sort_values("method_id")


def _condition_order(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result["condition_id"] = pd.Categorical(result["condition_id"], CONDITIONS, ordered=True)
    return result.sort_values("condition_id")


def _interval_plot(ax: plt.Axes, frame: pd.DataFrame, mean: str, low: str, high: str, *, xlabel: str, zero: bool = False) -> None:
    data = _method_order(frame)
    for y, (_, row) in enumerate(data.iterrows()):
        method = str(row["method_id"])
        value = float(row[mean])
        ax.errorbar(value, y, xerr=[[value-float(row[low])], [float(row[high])-value]], color=COLORS[method], marker=MARKERS[method], linestyle="none", capsize=3)
    ax.set_yticks(range(len(data)), [METHOD_LABELS[str(m)] for m in data["method_id"]])
    ax.set_xlabel(xlabel)
    if zero: ax.axvline(0, color="#333333", lw=0.8)


def _fig_rq1_summary(data: dict[str, pd.DataFrame], base: Path, field: str, defense: bool = False) -> list[Path]:
    _configure(13 if defense else 9)
    fig, ax = plt.subplots(figsize=(8.0 if defense else 6.3, 4.5 if defense else 3.6))
    if field == "final":
        _interval_plot(ax, data["pa_summary"], "final_mean", "final_ci_lower", "final_ci_upper", xlabel="Final mean return (higher is better)")
        ax.set_title("RQ1 final nominal performance")
    else:
        _interval_plot(ax, data["pa_summary"], "time_average_mean", "time_average_ci_lower", "time_average_ci_upper", xlabel="Interaction-axis time-average return (higher is better)")
        ax.set_title("RQ1 nominal learning efficiency")
    return _finish(fig, base)


def _fig_root_distribution(data: dict[str, pd.DataFrame], base: Path, field: str) -> list[Path]:
    _configure()
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    frame = data["pa_roots"]
    rng = np.random.default_rng(613)
    for x, method in enumerate(METHODS):
        values = frame.loc[frame.method_id == method, field].astype(float).to_numpy()
        ax.boxplot(values, positions=[x], widths=.5, showfliers=False, patch_artist=True, boxprops={"facecolor": COLORS[method], "alpha": .18}, medianprops={"color": COLORS[method]})
        jitter = rng.uniform(-.10, .10, len(values))
        ax.scatter(x+jitter, values, color=COLORS[method], marker=MARKERS[method], s=22, alpha=.85)
    ax.set_xticks(range(5), [METHOD_LABELS[m] for m in METHODS], rotation=20, ha="right")
    ax.set_ylabel("Return (higher is better)")
    ax.set_title("RQ1 root-level " + ("final-value" if field == "final_value" else "time-average") + " distribution")
    return _finish(fig, base)


def _fig_contrasts(data: dict[str, pd.DataFrame], base: Path, phase: str) -> list[Path]:
    _configure(7.5)
    key = {"rq1": "pa_contrasts", "rq2": "pb_contrasts", "rq3": "recovery_contrasts"}[phase]
    frame = data[key]
    if phase == "rq1":
        groups = [("phase-a-final-value", "Final value"), ("phase-a-time-average", "Time average")]
    elif phase == "rq2":
        groups = [(e, e.replace("phase-b-", "").replace("-", " ").title()) for e in sorted(frame.estimand.unique())]
    else:
        frame = frame[frame.primary_recovery_axis.astype(str).str.lower().isin(["true", "1"])]
        groups = [(e, e.replace("recovery-", "").replace("-", " ").title()) for e in sorted(frame.estimand.unique())]
    conditions = [None] if phase == "rq1" else ([c for c in CONDITIONS] if phase == "rq2" else CONDITIONS[:2])
    fig, axes = plt.subplots(
        len(groups),
        len(conditions),
        figsize=(5.0 * len(conditions), 4.8 * len(groups)),
        squeeze=False,
        constrained_layout=True,
    )
    for i, (estimand, title) in enumerate(groups):
        for j, condition in enumerate(conditions):
            ax = axes[i, j]
            subset = frame[frame.estimand == estimand]
            if condition is not None: subset = subset[subset.condition_id == condition]
            subset = subset.reset_index(drop=True)
            labels=[]
            for y,row in subset.iterrows():
                value=float(row.mean_difference); lo=float(row.ci_lower); hi=float(row.ci_upper)
                ax.errorbar(value,y,xerr=[[value-lo],[hi-value]],color="#3d3d3d",marker="o",capsize=2,linestyle="none")
                labels.append(f"{METHOD_LABELS[row.method_a]} − {METHOD_LABELS[row.method_b]}")
            ax.axvline(0,color="#333333",lw=.8)
            ax.set_yticks(range(len(labels)), labels)
            if i == len(groups) - 1:
                ax.set_xlabel("Root-paired A − B estimate (95% t interval)")
            ax.set_title(title + ("\n"+CONDITION_LABELS[condition] if condition else ""))
    fig.suptitle(phase.upper()+" declared direct method contrasts", y=1.005)
    return _finish(fig, base)


def _fig_adaptation(data: dict[str, pd.DataFrame], base: Path, small: bool = False, defense: bool = False) -> list[Path]:
    _configure(12.5 if defense else 8.5)
    frame=data["pb_summary"]
    if small:
        fig, axes=plt.subplots(2,2,figsize=(10,7),sharex=True,sharey=True); axes=axes.ravel()
        for ax,condition in zip(axes,CONDITIONS):
            sub=frame[frame.condition_id==condition]
            _interval_plot(ax,sub,"adaptation_benefit_mean","adaptation_benefit_ci_lower","adaptation_benefit_ci_upper",xlabel="Adaptation benefit",zero=True)
            ax.set_title(CONDITION_LABELS[condition])
    else:
        fig,ax=plt.subplots(figsize=(10 if defense else 8.2,5.5 if defense else 4.4))
        x=np.arange(len(CONDITIONS)); offsets=np.linspace(-.28,.28,5)
        for off,method in zip(offsets,METHODS):
            sub=_condition_order(frame[frame.method_id==method])
            y=sub.adaptation_benefit_mean.astype(float).to_numpy(); lo=sub.adaptation_benefit_ci_lower.astype(float).to_numpy(); hi=sub.adaptation_benefit_ci_upper.astype(float).to_numpy()
            ax.errorbar(x+off,y,yerr=[y-lo,hi-y],color=COLORS[method],marker=MARKERS[method],linestyle="none",capsize=2,label=METHOD_LABELS[method])
        ax.axhline(0,color="#333",lw=.8); ax.set_xticks(x,[CONDITION_LABELS[c] for c in CONDITIONS],rotation=18,ha="right")
        ax.set_ylabel("Adaptation benefit (higher is better)"); ax.set_title("RQ2 adaptation benefit by frozen condition"); _legend(ax,ncol=5)
    return _finish(fig,base)


def _fig_losses(data: dict[str,pd.DataFrame],base:Path,dumbbell:bool=False)->list[Path]:
    _configure(8)
    frame=data["pb_summary"]
    fig,axes=plt.subplots(2,2,figsize=(10,7),sharex=True); axes=axes.ravel()
    for ax,condition in zip(axes,CONDITIONS):
        sub=_method_order(frame[frame.condition_id==condition])
        y=np.arange(5)
        frozen=sub.frozen_loss_mean.astype(float).to_numpy(); adaptive=sub.adaptive_loss_mean.astype(float).to_numpy()
        if dumbbell:
            for i,(f,a,m) in enumerate(zip(frozen,adaptive,METHODS)):
                ax.plot([f,a],[i,i],color="#999",lw=1.3); ax.scatter(f,i,facecolors="white",edgecolors=COLORS[m],marker=MARKERS[m]); ax.scatter(a,i,color=COLORS[m],marker=MARKERS[m])
        else:
            ax.errorbar(frozen,y-.12,xerr=[frozen-sub.frozen_loss_ci_lower.astype(float),sub.frozen_loss_ci_upper.astype(float)-frozen],fmt="o",color="#666",capsize=2,label="Frozen" if condition==CONDITIONS[0] else None)
            ax.errorbar(adaptive,y+.12,xerr=[adaptive-sub.adaptive_loss_ci_lower.astype(float),sub.adaptive_loss_ci_upper.astype(float)-adaptive],fmt="s",color="#0072B2",capsize=2,label="Adaptive" if condition==CONDITIONS[0] else None)
        ax.set_yticks(y,[METHOD_LABELS[m] for m in METHODS]); ax.set_xlabel("Disturbance-associated loss (lower is better)"); ax.set_title(CONDITION_LABELS[condition])
    if dumbbell:
        axes[0].legend(
            handles=[
                Line2D([0], [0], color="#555", marker="o", markerfacecolor="white", linestyle="none", label="Frozen"),
                Line2D([0], [0], color="#0072B2", marker="o", linestyle="none", label="Adaptive"),
            ],
            frameon=False,
        )
    else:
        axes[0].legend(frameon=False)
    fig.suptitle("RQ2 Frozen and Adaptive losses" + (" (summary dumbbells)" if dumbbell else ""),y=1.005)
    return _finish(fig,base)


def _fig_pb_roots(data:dict[str,pd.DataFrame],base:Path,mode:str)->list[Path]:
    _configure(7.5); frame=data["pb_roots"]
    fig,axes=plt.subplots(2,2,figsize=(11,7),sharex=True); axes=axes.ravel()
    for ax,condition in zip(axes,CONDITIONS):
        sub=frame[frame.condition_id==condition]
        if mode=="benefit":
            vals=[sub[sub.method_id==m].adaptation_benefit.astype(float).to_numpy() for m in METHODS]
            ax.boxplot(vals,positions=np.arange(5),showfliers=False); 
            for x,(m,v) in enumerate(zip(METHODS,vals)): ax.scatter(np.full(len(v),x),v,s=10,color=COLORS[m],marker=MARKERS[m],alpha=.65)
            ax.axhline(0,color="#333",lw=.8); ax.set_ylabel("Adaptation benefit")
        else:
            for x,m in enumerate(METHODS):
                ms=sub[sub.method_id==m]
                for _,r in ms.iterrows(): ax.plot([x-.12,x+.12],[float(r.frozen_loss),float(r.adaptive_loss)],color=COLORS[m],alpha=.25,lw=.7)
                ax.scatter(np.full(len(ms),x-.12),ms.frozen_loss,s=8,facecolors="white",edgecolors=COLORS[m]); ax.scatter(np.full(len(ms),x+.12),ms.adaptive_loss,s=8,color=COLORS[m])
            ax.set_ylabel("Loss (Frozen left, Adaptive right)")
        ax.set_xticks(range(5),[METHOD_LABELS[m] for m in METHODS],rotation=25,ha="right"); ax.set_title(CONDITION_LABELS[condition])
    fig.suptitle("RQ2 root-level "+("adaptation-benefit distributions" if mode=="benefit" else "Frozen→Adaptive diagnostics"),y=1.005)
    return _finish(fig,base)


def _fig_heatmap(data:dict[str,pd.DataFrame],base:Path)->list[Path]:
    _configure(8); frame=data["pb_summary"]
    matrix=np.array([[float(frame[(frame.method_id==m)&(frame.condition_id==c)].adaptation_benefit_mean.iloc[0]) for c in CONDITIONS] for m in METHODS])
    fig,ax=plt.subplots(figsize=(8.2,4.4)); limit=max(abs(matrix.min()),abs(matrix.max()))
    im=ax.imshow(matrix,cmap="PuOr",vmin=-limit,vmax=limit,aspect="auto")
    for i in range(5):
        for j in range(4): ax.text(j,i,f"{matrix[i,j]:.2f}",ha="center",va="center",color="black")
    ax.set_xticks(range(4),[CONDITION_LABELS[c] for c in CONDITIONS],rotation=20,ha="right"); ax.set_yticks(range(5),[METHOD_LABELS[m] for m in METHODS]); ax.set_title("RQ2 adaptation benefit (higher is better)"); fig.colorbar(im,ax=ax,label="Adaptation benefit")
    return _finish(fig,base)


def _fig_recovery_summary(data:dict[str,pd.DataFrame],base:Path,metric:str,all_conditions:bool=False,defense:bool=False)->list[Path]:
    _configure(12.5 if defense else 8.5); frame=data["rec_summary"]
    conditions=CONDITIONS if all_conditions else CONDITIONS[:2]
    fig,axes=plt.subplots(1,len(conditions),figsize=((5.0 if defense else 4.4)*len(conditions),4.7 if defense else 3.8),sharey=metric=="proportion",squeeze=False)
    for ax,condition in zip(axes.ravel(),conditions):
        sub=_method_order(frame[frame.condition_id==condition])
        if metric=="proportion":
            vals=sub.recovered_proportion.astype(float).to_numpy(); ax.bar(range(5),vals,color=[COLORS[m] for m in METHODS],alpha=.78,hatch=["","//","..","xx","\\\\"]); ax.set_ylim(0,1.05); ax.set_ylabel("Recovered proportion")
            for x,(_,r) in enumerate(sub.iterrows()): ax.text(x,float(r.recovered_proportion)+.025,f"{int(r.recovered_root_count)}/{int(r.included_root_count)}",ha="center",fontsize=7)
        elif metric=="restricted": _interval_plot(ax,sub,"restricted_delay_mean","restricted_delay_ci_lower","restricted_delay_ci_upper",xlabel="Restricted recovery delay through 256 (lower is better)")
        else:
            valid=sub[sub.conditional_recovery_time_n.astype(int)>0]
            _interval_plot(ax,valid,"conditional_recovery_time_mean","conditional_recovery_time_ci_lower","conditional_recovery_time_ci_upper",xlabel="Observed recovery time, recovered roots only")
            for y,(_,r) in enumerate(_method_order(valid).iterrows()): ax.text(float(r.conditional_recovery_time_mean),y+.18,f"n={int(r.conditional_recovery_time_n)}",fontsize=7)
        if metric=="proportion": ax.set_xticks(range(5),[METHOD_LABELS[m] for m in METHODS],rotation=25,ha="right")
        ax.set_title(CONDITION_LABELS[condition])
    fig.suptitle({"proportion":"RQ3 stable recovery at primary tolerance 0.10","restricted":"RQ3 censoring-aware restricted recovery delay","conditional":"RQ3 observed recovery time conditional on recovery"}[metric],y=1.01)
    return _finish(fig,base)


def _fig_trajectories(data:dict[str,pd.DataFrame],base:Path,compact:bool)->list[Path]:
    _configure(6.5 if not compact else 7.5); frame=data["trajectories"]
    conditions=CONDITIONS[:2]
    fig,axes=plt.subplots(2 if compact else 5,1 if compact else 2,figsize=(10,7 if compact else 14),sharex=True,sharey=True,squeeze=False)
    if compact:
        for row,condition in enumerate(conditions):
            ax=axes[row,0]
            for method in METHODS:
                sub=frame[(frame.condition_id==condition)&(frame.method_id==method)]
                for _,root in sub.groupby("root_id",sort=True): ax.plot(root.window_end,root.directed_gap,color=COLORS[method],ls=LINESTYLES[method],alpha=.16,lw=.8)
            ax.axhline(.1,color="#222",ls="--",lw=.9,label="Tolerance 0.10"); ax.set_title(CONDITION_LABELS[condition]); ax.set_ylabel("Directed gap")
        _legend(axes[0,0],ncol=5)
    else:
        for i,method in enumerate(METHODS):
            for j,condition in enumerate(conditions):
                ax=axes[i,j]; sub=frame[(frame.condition_id==condition)&(frame.method_id==method)]
                for _,root in sub.groupby("root_id",sort=True): ax.plot(root.window_end,root.directed_gap,color=COLORS[method],alpha=.45,lw=.8)
                ax.axhline(.1,color="#222",ls="--",lw=.8); ax.set_title(f"{METHOD_LABELS[method]} — {CONDITION_LABELS[condition]}"); ax.set_ylabel("Directed gap")
    for ax in axes[-1,:]: ax.set_xlabel("Interaction (32-interaction windows; horizon 256)")
    fig.suptitle("RQ3 stored per-root recovery trajectories"+(" — primary overview" if compact else " — detailed audit"),y=.995)
    return _finish(fig,base)


def _fig_composition(data:dict[str,pd.DataFrame],base:Path)->list[Path]:
    _configure(8); frame=data["rec_summary"]
    fig,axes=plt.subplots(1,2,figsize=(10,4),sharey=True)
    for ax,condition in zip(axes,CONDITIONS[:2]):
        sub=_method_order(frame[frame.condition_id==condition]); rec=sub.recovered_root_count.astype(int); cens=sub.right_censored_root_count.astype(int)
        ax.bar(range(5),rec,color=[COLORS[m] for m in METHODS],label="Recovered"); ax.bar(range(5),cens,bottom=rec,color="#bdbdbd",hatch="//",label="Right-censored")
        ax.set_xticks(range(5),[METHOD_LABELS[m] for m in METHODS],rotation=25,ha="right"); ax.set_ylim(0,12.5); ax.set_title(CONDITION_LABELS[condition]); ax.set_ylabel("Roots")
    axes[0].legend(frameon=False); fig.suptitle("RQ3 recovered versus right-censored composition",y=1.01)
    return _finish(fig,base)


def _fig_sensitivity(data:dict[str,pd.DataFrame],base:Path,defense:bool=False)->list[Path]:
    _configure(12.5 if defense else 8.5); frame=data["sensitivity"]
    fig,axes=plt.subplots(1,2,figsize=(11 if defense else 8.8,4.8 if defense else 3.8),sharey=True)
    for ax,condition in zip(axes,CONDITIONS[:2]):
        for method in METHODS:
            sub=frame[(frame.condition_id==condition)&(frame.method_id==method)].sort_values("tolerance")
            ax.plot(sub.tolerance,sub.recovered_proportion,color=COLORS[method],marker=MARKERS[method],ls=LINESTYLES[method],label=METHOD_LABELS[method])
        ax.axvline(.1,color="#222",ls="--",lw=.8); ax.set_xticks([.05,.1,.2]); ax.set_ylim(-.03,1.03); ax.set_xlabel("Recovery tolerance (0.10 primary)"); ax.set_title(CONDITION_LABELS[condition]); ax.set_ylabel("Recovered proportion")
    _legend(axes[0],ncol=3); fig.suptitle("RQ3 predeclared tolerance sensitivity",y=1.01)
    return _finish(fig,base)


def _fig_timeline(data:dict[str,pd.DataFrame],base:Path)->list[Path]:
    _configure(7.5); frame=data["rec_roots"]; frame=frame[frame.primary_recovery_axis.astype(str).str.lower().isin(["true","1"])]
    fig,axes=plt.subplots(2,5,figsize=(14,6),sharex=True,sharey=True)
    roots=sorted(frame.root_id.unique())
    for i,condition in enumerate(CONDITIONS[:2]):
        for j,method in enumerate(METHODS):
            ax=axes[i,j]; sub=frame[(frame.condition_id==condition)&(frame.method_id==method)].set_index("root_id").loc[roots]
            for y,(_,r) in enumerate(sub.iterrows()):
                if r.status=="recovered":
                    ax.plot([float(r.recovery_time),float(r.confirmation_time)],[y,y],color=COLORS[method],lw=1); ax.scatter(float(r.recovery_time),y,color=COLORS[method],marker="o",s=13); ax.scatter(float(r.confirmation_time),y,facecolors="white",edgecolors=COLORS[method],marker="s",s=13)
                else: ax.scatter(256,y,color="#777",marker="|",s=35)
            ax.set_title(METHOD_LABELS[method]+"\n"+CONDITION_LABELS[condition]); ax.set_yticks(range(12),[r.rsplit("r",1)[-1] for r in roots]); ax.set_xlim(0,260)
    for ax in axes[-1]: ax.set_xlabel("Interaction")
    fig.suptitle("RQ3 stored recovery/confirmation timeline; | = right-censored at 256",y=1.01)
    return _finish(fig,base)


def _diagram(base:Path,title:str,boxes:list[str],arrows:bool=True)->list[Path]:
    _configure(9); fig,ax=plt.subplots(figsize=(11,3.2)); ax.axis("off")
    n=len(boxes); width=.14
    for i,text in enumerate(boxes):
        x=.04+i*(.92/n); patch=FancyBboxPatch((x,.38),width,.25,boxstyle="round,pad=0.025",fc="#e9f2f7",ec="#0072B2",lw=1.2,transform=ax.transAxes); ax.add_patch(patch); ax.text(x+width/2,.505,text,ha="center",va="center",transform=ax.transAxes,wrap=True)
        if arrows and i<n-1: ax.add_patch(FancyArrowPatch((x+width+.005,.505),(x+.92/n-.005,.505),arrowstyle="->",mutation_scale=13,color="#555",transform=ax.transAxes))
    ax.set_title(title,pad=15)
    return _finish(fig,base)


def _fig_all_rq(data:dict[str,pd.DataFrame],base:Path)->list[Path]:
    _configure(9.5); fig,axes=plt.subplots(1,3,figsize=(14,4.3))
    pa=_method_order(data["pa_summary"]); axes[0].bar(range(5),pa.final_mean,color=[COLORS[m] for m in METHODS]); axes[0].set_xticks(range(5),[METHOD_LABELS[m] for m in METHODS],rotation=35,ha="right"); axes[0].set_title("RQ1: final return\n(higher is better)")
    pb=data["pb_summary"]; x=np.arange(5)
    for off,c in zip([-.18,.18],CONDITIONS[:2]):
        sub=_method_order(pb[pb.condition_id==c]); axes[1].scatter(x+off,sub.adaptation_benefit_mean,label=CONDITION_LABELS[c],marker="o" if off<0 else "s")
    axes[1].axhline(0,color="#333",lw=.8); axes[1].set_xticks(x,[METHOD_LABELS[m] for m in METHODS],rotation=35,ha="right"); axes[1].set_title("RQ2: remap adaptation benefit\n(higher is better)"); axes[1].legend(frameon=False,fontsize=7)
    rec=data["rec_summary"]
    for off,c in zip([-.18,.18],CONDITIONS[:2]):
        sub=_method_order(rec[rec.condition_id==c]); axes[2].scatter(x+off,sub.recovered_proportion,label=CONDITION_LABELS[c],marker="o" if off<0 else "s")
    axes[2].set_ylim(0,1.05); axes[2].set_xticks(x,[METHOD_LABELS[m] for m in METHODS],rotation=35,ha="right"); axes[2].set_title("RQ3: recovered proportion\n(primary tolerance 0.10)"); axes[2].legend(frameon=False,fontsize=7)
    fig.suptitle("Descriptive protocol-v2.1 overview — panels are distinct estimands; no composite ranking",y=1.01)
    return _finish(fig,base)


@dataclass(frozen=True)
class FigureSpec:
    asset_id: str
    category: int
    rq: str
    estimand: str
    use: list[str]
    source_keys: list[str]
    caption: str
    render: Callable[[dict[str,pd.DataFrame],Path],list[Path]]


def _figure_specs() -> list[FigureSpec]:
    return [
        FigureSpec("FIG-RQ1-002-FINAL",2,"RQ1","phase-a-final-value",["main-thesis"],["pa_summary"],"Final nominal return by method with pointwise 95% Student-t intervals over 12 roots.",lambda d,p:_fig_rq1_summary(d,p,"final")),
        FigureSpec("FIG-RQ1-003-TIME-AVERAGE",3,"RQ1","phase-a-time-average",["main-thesis"],["pa_summary"],"Interaction-axis time-average return, kept separate from final performance.",lambda d,p:_fig_rq1_summary(d,p,"time")),
        FigureSpec("FIG-RQ1-004-FINAL-ROOTS",4,"RQ1","phase-a-final-value",["appendix"],["pa_roots"],"Root-level final nominal-return distribution after equal-layout reduction.",lambda d,p:_fig_root_distribution(d,p,"final_value")),
        FigureSpec("FIG-RQ1-005-TIME-ROOTS",5,"RQ1","phase-a-time-average",["appendix"],["pa_roots"],"Root-level time-average return distribution after equal-layout reduction.",lambda d,p:_fig_root_distribution(d,p,"time_average")),
        FigureSpec("FIG-RQ1-007-CONTRASTS",7,"RQ1","declared-root-paired-contrasts",["appendix"],["pa_contrasts"],"Declared root-paired A-minus-B contrasts; intervals are descriptive pointwise t intervals.",lambda d,p:_fig_contrasts(d,p,"rq1")),
        FigureSpec("FIG-RQ2-008-ADAPTATION",8,"RQ2","adaptation-benefit",["main-thesis"],["pb_summary"],"Adaptation benefit by method and frozen condition; positive values mean lower Adaptive than Frozen loss.",lambda d,p:_fig_adaptation(d,p)),
        FigureSpec("FIG-RQ2-009-LOSSES",9,"RQ2","frozen-loss;adaptive-loss",["main-thesis"],["pb_summary"],"Frozen and Adaptive disturbance-associated loss remain distinct quantities.",lambda d,p:_fig_losses(d,p)),
        FigureSpec("FIG-RQ2-010-CONDITIONS",10,"RQ2","adaptation-benefit",["main-thesis","appendix"],["pb_summary"],"Condition-small-multiple view of adaptation benefit on consistent scales.",lambda d,p:_fig_adaptation(d,p,small=True)),
        FigureSpec("FIG-RQ2-011-DUMBBELLS",11,"RQ2","frozen-loss;adaptive-loss",["appendix"],["pb_summary"],"Summary Frozen-to-Adaptive dumbbells by method and condition.",lambda d,p:_fig_losses(d,p,dumbbell=True)),
        FigureSpec("FIG-RQ2-012-BENEFIT-ROOTS",12,"RQ2","adaptation-benefit",["appendix"],["pb_roots"],"Root-level adaptation-benefit distributions by method and condition.",lambda d,p:_fig_pb_roots(d,p,"benefit")),
        FigureSpec("FIG-RQ2-013-HEATMAP",13,"RQ2","adaptation-benefit",["appendix"],["pb_summary"],"Numeric heatmap of stored mean adaptation benefit; higher is better.",_fig_heatmap),
        FigureSpec("FIG-RQ2-014-CONTRASTS",14,"RQ2","declared-root-paired-contrasts",["appendix"],["pb_contrasts"],"All declared RQ2 root-paired A-minus-B contrasts by condition and estimand.",lambda d,p:_fig_contrasts(d,p,"rq2")),
        FigureSpec("FIG-RQ2-015-PAIRED-ROOTS",15,"RQ2","frozen-loss;adaptive-loss",["appendix"],["pb_roots"],"Root-level Frozen-to-Adaptive paired diagnostics; connecting lines do not imply an additional estimand.",lambda d,p:_fig_pb_roots(d,p,"paired")),
        FigureSpec("FIG-RQ3-016-TRAJECTORIES",16,"RQ3","directed-gap-trajectory",["main-thesis"],["trajectories"],"Stored per-root directed-gap trajectories for the primary action-remap family; dashed line is tolerance 0.10.",lambda d,p:_fig_trajectories(d,p,True)),
        FigureSpec("FIG-RQ3-017-RECOVERED",17,"RQ3","recovered-proportion",["main-thesis"],["rec_summary"],"Recovered roots at primary tolerance 0.10; unrecovered roots remain right-censored.",lambda d,p:_fig_recovery_summary(d,p,"proportion")),
        FigureSpec("FIG-RQ3-018-RESTRICTED",18,"RQ3","restricted-recovery-delay",["main-thesis"],["rec_summary"],"Censoring-aware restricted recovery delay through the 256-interaction horizon.",lambda d,p:_fig_recovery_summary(d,p,"restricted")),
        FigureSpec("FIG-RQ3-019-CONDITIONAL",19,"RQ3","conditional-recovery-time",["main-thesis"],["rec_summary"],"Observed recovery time only among recovered roots; displayed n excludes right-censored roots.",lambda d,p:_fig_recovery_summary(d,p,"conditional")),
        FigureSpec("FIG-RQ3-020-CONDITIONS",20,"RQ3","recovered-proportion",["appendix"],["rec_summary"],"Recovery proportion across all frozen conditions; action-remaps are the primary recovery axis.",lambda d,p:_fig_recovery_summary(d,p,"proportion",True)),
        FigureSpec("FIG-RQ3-021-ROOT-TRAJECTORIES",21,"RQ3","directed-gap-trajectory",["appendix"],["trajectories"],"Detailed stored root trajectories by method and primary condition; no trajectory averaging.",lambda d,p:_fig_trajectories(d,p,False)),
        FigureSpec("FIG-RQ3-022-CENSORING",22,"RQ3","recovery-status",["appendix"],["rec_summary"],"Recovered versus right-censored root composition at tolerance 0.10.",_fig_composition),
        FigureSpec("FIG-RQ3-023-SENSITIVITY",23,"RQ3","recovered-proportion-sensitivity",["main-thesis","appendix"],["sensitivity"],"Predeclared 0.05/0.10/0.20 tolerance sensitivity; 0.10 remains primary.",_fig_sensitivity),
        FigureSpec("FIG-RQ3-024-CONTRASTS",24,"RQ3","declared-root-paired-contrasts",["appendix"],["recovery_contrasts"],"Declared recovery-status and restricted-delay A-minus-B contrasts on the primary axis.",lambda d,p:_fig_contrasts(d,p,"rq3")),
        FigureSpec("FIG-RQ3-025-TIMELINE",25,"RQ3","recovery-time;confirmation-time;censoring",["appendix"],["rec_roots"],"Stored recovery and confirmation times; right-censored roots are marked at the horizon without fake recovery times.",_fig_timeline),
        FigureSpec("FIG-METHOD-026-EXPERIMENT-FLOW",26,"methodology","protocol-flow",["main-thesis","defense"],["analysis_manifest"],"Protocol flow; exact checkpoints precede matched FN/FD/AN/AD branches.",lambda d,p:_diagram(p,"Protocol-v2.1 experiment flow",["Phase A\nnominal learning","Exact checkpoint","Matched FN / FD / AN / AD","Validation","Root-level analysis","Registered exports"])),
        FigureSpec("FIG-METHOD-027-RQ-MAP",27,"methodology","rq-evidence-map",["main-thesis","defense"],["analysis_manifest"],"Map from each research question to its frozen estimands and registered outputs.",lambda d,p:_diagram(p,"Research questions to evidence",["RQ1\nfinal + time average","RQ2\nFrozen loss + Adaptive loss + benefit","RQ3\nstatus + restricted delay + conditional time","Root-paired contrasts","Figures + tables"])),
        FigureSpec("FIG-METHOD-028-LINEAGE",28,"methodology","evidence-lineage",["main-thesis","appendix","defense"],["freeze_manifest","analysis_manifest"],"Accepted-evidence lineage; the failed 216-job attempt is excluded.",lambda d,p:_diagram(p,"Accepted evidence lineage",["Frozen\nrecipe","603/603\nreplacement jobs","T-611\nvalidation + freeze","T-612\nanalysis package","T-613\nassets"])),
        FigureSpec("FIG-DEF-029-ALL-RQ",29,"cross-RQ","distinct-panel-descriptive-summary",["defense"],["pa_summary","pb_summary","rec_summary"],"Defense-only overview with distinct panels and no composite score or universal ranking.",_fig_all_rq),
        FigureSpec("FIG-DEF-030-RQ1-FINAL",30,"RQ1","phase-a-final-value",["defense"],["pa_summary"],"Large-label defense variant of the RQ1 final-performance figure.",lambda d,p:_fig_rq1_summary(d,p,"final",True)),
        FigureSpec("FIG-DEF-030-RQ2-ADAPTATION",30,"RQ2","adaptation-benefit",["defense"],["pb_summary"],"Large-label defense variant of the RQ2 adaptation-benefit figure.",lambda d,p:_fig_adaptation(d,p,defense=True)),
        FigureSpec("FIG-DEF-030-RQ3-RECOVERED",30,"RQ3","recovered-proportion",["defense"],["rec_summary"],"Large-label defense variant of the RQ3 recovered-proportion figure.",lambda d,p:_fig_recovery_summary(d,p,"proportion",defense=True)),
        FigureSpec("FIG-DEF-030-RQ3-SENSITIVITY",30,"RQ3","recovered-proportion-sensitivity",["defense"],["sensitivity"],"Large-label defense variant of the predeclared tolerance-sensitivity figure.",lambda d,p:_fig_sensitivity(d,p,True)),
    ]


def _source_map(repo_root:Path)->dict[str,dict[str,Any]]:
    manifest=_json(repo_root/ANALYSIS_MANIFEST_RELATIVE)
    by_name={Path(x["relative_path"]).name:x for x in manifest["canonical_analysis_artifacts"]}
    mapping={
        "pa_summary":by_name["phase-a-method-summary.csv"], "pa_roots":by_name["phase-a-root-records.csv"], "pa_contrasts":by_name["phase-a-method-contrasts.csv"],
        "pb_summary":by_name["phase-b-method-condition-summary.csv"], "pb_roots":by_name["phase-b-root-records.csv"], "pb_contrasts":by_name["phase-b-method-contrasts.csv"],
        "rec_summary":by_name["recovery-method-condition-summary.csv"], "rec_roots":by_name["recovery-root-records.csv"], "recovery_contrasts":by_name["recovery-method-contrasts.csv"],
        "trajectories":by_name["recovery-trajectory-records.csv"], "sensitivity":{"relative_path":str(DIAGNOSTICS_RELATIVE).replace("\\","/"),"sha256":_sha(repo_root/DIAGNOSTICS_RELATIVE)},
        "analysis_manifest":{"relative_path":str(ANALYSIS_MANIFEST_RELATIVE).replace("\\","/"),"sha256":_sha(repo_root/ANALYSIS_MANIFEST_RELATIVE)},
        "freeze_manifest":{"relative_path":str(FREEZE_MANIFEST_RELATIVE).replace("\\","/"),"sha256":_sha(repo_root/FREEZE_MANIFEST_RELATIVE)},
    }
    return mapping


def _load_data(repo_root:Path)->dict[str,pd.DataFrame]:
    export=repo_root/STUDY_EXPORT_RELATIVE
    diagnostics=_json(repo_root/DIAGNOSTICS_RELATIVE)
    return {
        "pa_summary":pd.read_csv(export/"phase-a-method-summary.csv"), "pa_roots":pd.read_csv(export/"phase-a-root-records.csv"), "pa_contrasts":pd.read_csv(export/"phase-a-method-contrasts.csv"),
        "pb_summary":pd.read_csv(export/"phase-b-method-condition-summary.csv"), "pb_roots":pd.read_csv(export/"phase-b-root-records.csv"), "pb_contrasts":pd.read_csv(export/"phase-b-method-contrasts.csv"),
        "rec_summary":pd.read_csv(export/"recovery-method-condition-summary.csv"), "rec_roots":pd.read_csv(export/"recovery-root-records.csv"), "recovery_contrasts":pd.read_csv(export/"recovery-method-contrasts.csv"),
        "trajectories":pd.read_csv(export/"recovery-trajectory-records.csv"), "sensitivity":pd.DataFrame(diagnostics["recovery_sensitivity_primary_action_remap"]),
    }


def _markdown_table(csv_path:Path,md_path:Path)->None:
    frame=pd.read_csv(csv_path,keep_default_na=False)
    headers=list(frame.columns)
    def esc(value:Any)->str: return str(value).replace("|","\\|").replace("\n"," ")
    lines=["| "+" | ".join(map(esc,headers))+" |","| "+" | ".join(["---"]*len(headers))+" |"]
    lines += ["| "+" | ".join(esc(row[h]) for h in headers)+" |" for _,row in frame.iterrows()]
    md_path.write_text("\n".join(lines)+"\n",encoding="utf-8",newline="\n")


def _write_tables(repo_root:Path,out:Path,sources:dict[str,dict[str,Any]])->list[dict[str,Any]]:
    table_dir=out/"tables"; table_dir.mkdir(parents=True,exist_ok=True); entries=[]
    analysis_manifest = _json(repo_root / ANALYSIS_MANIFEST_RELATIVE)
    canonical_by_name = {
        Path(record["relative_path"]).name: record
        for record in analysis_manifest["canonical_analysis_artifacts"]
    }
    for source in sorted((repo_root/STUDY_EXPORT_RELATIVE).glob("*.csv")):
        csv_out=table_dir/source.name; shutil.copyfile(source,csv_out); md_out=table_dir/(source.stem+".md"); _markdown_table(csv_out,md_out)
        artifact = canonical_by_name[source.name]
        entries.append({"asset_id":"TABLE-"+source.stem.upper().replace("-","_"),"kind":"table","rq_scope":"RQ1/RQ2/RQ3" if "root" in source.name else "registered-analysis","estimand_scope":"canonical-T612-export","intended_use":["appendix","machine-readable"],"source_artifacts":[artifact],"outputs":[]})
        entries[-1]["outputs"]=[{"relative_path":str(p.relative_to(out)).replace("\\","/"),"sha256":_sha(p),"size_bytes":p.stat().st_size,"format":p.suffix[1:]} for p in (csv_out,md_out)]
    sensitivity=_json(repo_root/DIAGNOSTICS_RELATIVE)["recovery_sensitivity_primary_action_remap"]
    csv_out=table_dir/"recovery-tolerance-sensitivity-summary.csv"
    with csv_out.open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=list(sensitivity[0]),lineterminator="\n"); writer.writeheader(); writer.writerows(sensitivity)
    md_out=table_dir/"recovery-tolerance-sensitivity-summary.md"; _markdown_table(csv_out,md_out)
    entries.append({"asset_id":"TABLE-RQ3-TOLERANCE-SENSITIVITY","kind":"table","rq_scope":"RQ3","estimand_scope":"recovered-proportion-sensitivity","intended_use":["main-thesis","appendix","machine-readable"],"source_artifacts":[sources["sensitivity"]],"outputs":[{"relative_path":str(p.relative_to(out)).replace("\\","/"),"sha256":_sha(p),"size_bytes":p.stat().st_size,"format":p.suffix[1:]} for p in (csv_out,md_out)]})
    return entries


def _verify_authorities(repo_root:Path)->tuple[dict[str,Any],dict[str,Any]]:
    freeze=validate_protocol_v21_final_freeze(repo_root)
    analysis=verify_protocol_v21_t612(repo_root)
    if freeze["freeze_manifest_sha256"]!=EXPECTED_FREEZE_SHA or freeze["run_manifest_inventory_sha256"]!=EXPECTED_INVENTORY_SHA: raise ValueError("T-611 authority identity mismatch")
    if _sha(repo_root/ANALYSIS_MANIFEST_RELATIVE)!=EXPECTED_ANALYSIS_SHA: raise ValueError("T-612 manifest identity mismatch")
    manifest=_json(repo_root/ANALYSIS_MANIFEST_RELATIVE)
    if manifest["historical_failed_attempt"]["used_as_scientific_input"] or manifest["historical_failed_attempt"]["eligible"]: raise ValueError("Historical failed attempt exclusion invariant failed")
    if set(manifest["rq_coverage"])!={"RQ1","RQ2","RQ3"} or manifest["recovery_tolerances"]!=[0.05,0.1,0.2]: raise ValueError("T-612 coverage invariant failed")
    return freeze,analysis


def generate_final_assets(repo_root:Path,output:Path|None,generator_commit:str)->dict[str,Any]:
    _verify_authorities(repo_root)
    out=(output if output else repo_root/PACKAGE_RELATIVE).resolve()
    if out.exists(): shutil.rmtree(out)
    (out/"figures").mkdir(parents=True)
    data=_load_data(repo_root); sources=_source_map(repo_root); assets=[]; captions=[]
    for spec in _figure_specs():
        base=out/"figures"/spec.asset_id.lower()
        paths=spec.render(data,base)
        assets.append({"asset_id":spec.asset_id,"inventory_category":spec.category,"kind":"figure","rq_scope":spec.rq,"estimand_scope":spec.estimand,"condition_scope":"frozen-protocol-scope","intended_use":spec.use,"caption":spec.caption,"source_artifacts":[sources[k] for k in spec.source_keys],"presentation_parameters":{"method_order":METHODS,"condition_order":CONDITIONS,"colorblind_safe_palette":COLORS,"redundant_markers":MARKERS,"raster_dpi":300},"outputs":[{"relative_path":str(p.relative_to(out)).replace("\\","/"),"sha256":_sha(p),"size_bytes":p.stat().st_size,"format":p.suffix[1:]} for p in paths]})
        captions.append(f"### {spec.asset_id}\n\n{spec.caption}\n")
    assets.extend(_write_tables(repo_root,out,sources))
    unsupported=[
        {"inventory_category":1,"requested_asset":"RQ1 learning progression / probe curves by method","status":"unavailable","reason":"The finalized T-612 package contains final-value and interaction-axis time-average summaries but no registered probe/checkpoint-series values or intervals. T-613 does not read unfrozen alternate inputs or reconstruct a post-hoc trajectory."},
        {"inventory_category":6,"requested_asset":"RQ1 checkpoint/probe heatmap or compact matrix","status":"unavailable","reason":"No validated probe/checkpoint matrix is registered in the T-612 outputs. Endpoint values cannot be expanded into a checkpoint matrix without inventing data."},
    ]
    (out/"captions.md").write_text("# T-613 asset captions\n\nThese captions are technical asset guidance, not thesis Results/Discussion prose.\n\n"+"\n".join(captions),encoding="utf-8",newline="\n")
    (out/"inventory-disposition.json").write_bytes(_canonical_json({"supported_categories":sorted({a.get("inventory_category") for a in assets if a.get("inventory_category")}),"unsupported":unsupported}))
    generator_files=[Path("scripts/generate_protocol_v21_final_assets.py"),Path("src/resilient_agents/evidence_v2/final_assets.py")]
    manifest={
        "schema_version":1,"task_id":"T-613","status":"finalized","package_id":"protocol-v2.1-final-t613-assets-v1","scientific_recipe_id":"protocol-v2.1-final","accepted_execution_instance_id":"protocol-v2.1-final--t610-recovery-01",
        "t611_freeze_manifest_sha256":EXPECTED_FREEZE_SHA,"t611_run_manifest_inventory_sha256":EXPECTED_INVENTORY_SHA,"t612_analysis_manifest_sha256":EXPECTED_ANALYSIS_SHA,
        "generator":{"version":GENERATOR_VERSION,"git_commit":generator_commit,"source_files":[{"relative_path":str(p).replace("\\","/"),"sha256":_sha(repo_root/p)} for p in generator_files],"matplotlib_version":matplotlib.__version__},
        "deterministic_parameters":{"method_order":METHODS,"condition_order":CONDITIONS,"raster_dpi":300,"svg_hashsalt":"protocol-v2.1-final-t613","fixed_random_seed_for_display_jitter":613},
        "scientific_boundary":{"presentation_only":True,"new_estimands_computed":False,"right_censoring_preserved":True,"non_recovery_as_horizon_prohibited":True,"historical_failed_attempt_used":False,"application_screenshots_are_quantitative_sources":False,"t700_or_wp7_work_performed":False},
        "inventory":{"categories_total":30,"supported_categories":28,"unsupported_categories":[1,6],"unsupported_dispositions":unsupported},"assets":assets,
    }
    manifest_path=out/"asset-manifest.json"; manifest_path.write_bytes(_canonical_json(manifest)); manifest_sha=_sha(manifest_path)
    (out/"FINALIZED").write_text(manifest_sha+"  asset-manifest.json\n",encoding="ascii",newline="\n")
    validation=validate_final_assets(repo_root,out)
    return {**validation,"generated":True,"asset_manifest_sha256":manifest_sha}


def validate_final_assets(repo_root:Path,output:Path|None=None)->dict[str,Any]:
    _verify_authorities(repo_root)
    out=(output if output else repo_root/PACKAGE_RELATIVE).resolve(); manifest_path=out/"asset-manifest.json"; manifest=_json(manifest_path)
    finalized=(out/"FINALIZED").read_text(encoding="ascii").split()[0]
    if finalized!=_sha(manifest_path): raise ValueError("T-613 FINALIZED manifest hash mismatch")
    if manifest["t611_freeze_manifest_sha256"]!=EXPECTED_FREEZE_SHA or manifest["t612_analysis_manifest_sha256"]!=EXPECTED_ANALYSIS_SHA: raise ValueError("T-613 upstream provenance mismatch")
    if manifest["scientific_boundary"]["historical_failed_attempt_used"] or not manifest["scientific_boundary"]["right_censoring_preserved"]: raise ValueError("T-613 scientific boundary mismatch")
    if manifest["inventory"]["supported_categories"]!=28 or manifest["inventory"]["unsupported_categories"]!=[1,6]: raise ValueError("T-613 inventory disposition mismatch")
    seen=set(); output_count=0
    for asset in manifest["assets"]:
        if asset["asset_id"] in seen: raise ValueError(f"Duplicate asset id {asset['asset_id']}")
        seen.add(asset["asset_id"])
        for source in asset["source_artifacts"]:
            source_path=repo_root/source["relative_path"]
            if _sha(source_path)!=source["sha256"]: raise ValueError(f"Source changed: {source_path}")
        for item in asset["outputs"]:
            path=out/item["relative_path"]
            if _sha(path)!=item["sha256"] or path.stat().st_size!=item["size_bytes"]: raise ValueError(f"Output changed: {path}")
            output_count+=1
    for source in manifest["generator"]["source_files"]:
        if _sha(repo_root/source["relative_path"])!=source["sha256"]: raise ValueError("Generator source bytes differ from manifest")
    root_records=pd.read_csv(repo_root/STUDY_EXPORT_RELATIVE/"recovery-root-records.csv",keep_default_na=False)
    censored=root_records[root_records.status!="recovered"]
    if not censored.recovery_time.eq("").all(): raise ValueError("Right-censored recovery_time must remain null")
    return {"valid":True,"asset_count":len(manifest["assets"]),"output_file_count":output_count,"figure_count":sum(a["kind"]=="figure" for a in manifest["assets"]),"table_count":sum(a["kind"]=="table" for a in manifest["assets"]),"supported_inventory_categories":manifest["inventory"]["supported_categories"],"unsupported_inventory_categories":manifest["inventory"]["unsupported_categories"],"asset_manifest_sha256":_sha(manifest_path)}
