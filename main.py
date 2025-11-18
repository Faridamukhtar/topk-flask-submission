from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint
from collections import Counter
from typing import List, Dict, Any

app = FastAPI(title="Top K Frequent Elements API")

class TopKRequest(BaseModel):
    nums: List[Any]       # could restrict to int | str if you like
    k: conint(gt=0)       # k > 0

class TopKResponse(BaseModel):
    top_k: List[Any]
    frequencies: Dict[str, int]


@app.post("/top-k-frequent", response_model=TopKResponse)
def top_k_frequent(payload: TopKRequest):
    nums = payload.nums
    k = payload.k

    if not nums:
        raise HTTPException(status_code=400, detail="nums must not be empty")

    # Count frequencies
    freq = Counter(nums)

    if k > len(freq):
        raise HTTPException(
            status_code=400,
            detail=f"k={k} is greater than the number of distinct elements={len(freq)}"
        )

    # Get top k frequent elements
    # most_common returns list of (element, count) tuples
    most_common = freq.most_common(k)
    top_k = [elem for elem, _ in most_common]

    # Convert keys to string for JSON map
    frequencies = {str(elem): count for elem, count in freq.items()}

    return TopKResponse(top_k=top_k, frequencies=frequencies)
