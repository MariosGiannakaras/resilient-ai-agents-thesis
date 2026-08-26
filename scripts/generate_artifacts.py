import sys
import json
from pathlib import Path
import pandas as pd
import plotly.express as px

def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    analysis_dir = repo_root / "results" / "summaries" / "thesis-final-analysis"
    
    if not analysis_dir.exists():
        print(f"Error: {analysis_dir} not found.", file=sys.stderr)
        return 1
        
    artifacts_dir = repo_root / "results" / "thesis-final" / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    units_file = analysis_dir / "units.jsonl"
    if not units_file.exists():
        print(f"Error: {units_file} not found.", file=sys.stderr)
        return 1
        
    units = []
    with units_file.open("r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            metrics = obj.get("primary_metrics", {})
            units.append({
                "agent_id": obj["agent_id"],
                "condition_id": obj["condition_id"],
                "layout_id": obj["layout_id"],
                "run_id": obj["run_id"],
                "nominal_mean": metrics.get("nominal_mean", 0.0),
                "post_change_mean": metrics.get("post_change_mean", 0.0),
                "cumulative_deficit": metrics.get("cumulative_deficit", 0.0),
                "immediate_degradation": metrics.get("immediate_degradation", 0.0)
            })
            
    df = pd.DataFrame(units)
    
    # 1. Export raw primary metrics table
    csv_path = artifacts_dir / "primary_metrics.csv"
    df.to_csv(csv_path, index=False)
    print(f"Exported {csv_path.name}")
    
    # 2. Aggregated summary table
    summary_df = df.groupby(["agent_id", "condition_id"]).agg({
        "nominal_mean": ["mean", "std"],
        "post_change_mean": ["mean", "std"],
        "cumulative_deficit": ["mean", "std"],
        "immediate_degradation": ["mean", "std"]
    }).round(3)
    
    summary_csv_path = artifacts_dir / "aggregated_summary.csv"
    summary_df.to_csv(summary_csv_path)
    print(f"Exported {summary_csv_path.name}")
    
    # 3. Cumulative Deficit Boxplot
    fig1 = px.box(
        df, 
        x="condition_id", 
        y="cumulative_deficit", 
        color="agent_id",
        title="Cumulative Deficit by Condition and Agent",
        labels={
            "condition_id": "Condition",
            "cumulative_deficit": "Cumulative Deficit",
            "agent_id": "Agent"
        }
    )
    fig1.write_html(artifacts_dir / "cumulative_deficit_boxplot.html")
    
    # 4. Immediate Degradation Boxplot
    fig2 = px.box(
        df, 
        x="condition_id", 
        y="immediate_degradation", 
        color="agent_id",
        title="Immediate Degradation by Condition and Agent",
        labels={
            "condition_id": "Condition",
            "immediate_degradation": "Immediate Degradation",
            "agent_id": "Agent"
        }
    )
    fig2.write_html(artifacts_dir / "immediate_degradation_boxplot.html")
    
    print(f"Exported figures to {artifacts_dir.relative_to(repo_root)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
