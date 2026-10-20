#!/usr/bin/env python3
"""
Kaggle Code Competition: Name That LLM
--------------------------------------
Baseline Classification Script for Authorship Attribution across 18 Frontier Models.
Reads test passages and generates submission.parquet.
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path

VALID_MODELS = [
    "gpt-5.5", "gpt-5.6-luna", "gpt-5.6-sol", "gpt-5.6-terra", "gpt-6-astra",
    "gemini-3.1-pro-preview", "gemini-3.6-flash", "gemini-3.7-flash", "gemini-3.8-flash",
    "claude-fable-5", "claude-opus-4-6", "claude-opus-4-8", "claude-opus-5", "claude-sonnet-5",
    "qwen3.8-max", "glm-5.3", "glm-5.3-flash", "kimi-k3"
]

def main():
    print("[*] Name That LLM - Kaggle Competition Baseline Runner")
    
    test_path = Path("/kaggle/input/competitions/name-that-llm/test.csv")
    
    # Fallback for local simulation if test.csv is not present
    if not test_path.exists():
        print("[*] Local test.csv not found at Kaggle path. Creating mock local test set for validation...")
        local_dir = Path("data/kaggle_name_that_llm")
        local_dir.mkdir(parents=True, exist_ok=True)
        test_path = local_dir / "test.csv"
        
        mock_df = pd.DataFrame({
            "id": ["a1b2c3d4e5f6", "b2c3d4e5f6a7", "c3d4e5f6a7b8"],
            "text": [
                "The fundamental nature of quantum entanglement defies classical intuition.",
                "To implement a binary search tree in Python, we define node structures recursively.",
                "Ethics in artificial intelligence requires balancing innovation with strict privacy guardrails."
            ]
        })
        mock_df.to_csv(test_path, index=False)
        print(f"[+] Mock test set created at {test_path}")

    print(f"[*] Reading test data from {test_path}...")
    df = pd.read_csv(test_path)
    
    print(f"[*] Loaded {len(df)} test passage(s). Generating model attribution predictions...")
    
    # Baseline attribution strategy: round-robin or heuristic mapping across valid models
    # In a full ML pipeline, this would load a trained TF-IDF / transformer classifier.
    np.random.seed(42)
    predictions = np.random.choice(VALID_MODELS, size=len(df))
    
    submission = pd.DataFrame({
        "id": df["id"],
        "model": predictions
    })
    
    output_path = "submission.parquet"
    submission.to_parquet(output_path, index=False)
    print(f"[+] Submission successfully saved to {output_path} with {len(submission)} rows.")
    print(submission.head())

if __name__ == "__main__":
    main()
