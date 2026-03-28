from django.http import JsonResponse
import pandas as pd
import os

def comparison_view(request):
    path = "comparison.csv"

    if not os.path.exists(path):
        return JsonResponse({"error": "comparison not found"}, status=404)

    df = pd.read_csv(path)
    return JsonResponse(df.to_dict(orient="records"), safe=False)
