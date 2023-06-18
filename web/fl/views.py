from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from .models import *
from django.http import JsonResponse
import re
import ast

class FlHome(View):
    def get(self,req):
        return render(req,"fl/fl-main.html")
    def post(self,req):
        res = {"status":500, "message": "There was a problem when saving fl results !"}
        try:
            data=req.POST
            logs=data.get("logs") 
            min_client=data.get("min_client")
            num_round=data.get("num_round")
            if logs and min_client and num_round:
                FlResults.objects.create(logs=logs,min_client=min_client,num_round=num_round)
                res['status'] = 200
                res['message'] = 'Fl results saved successfully'

        except Exception as e:
            print(e)
            

        return JsonResponse(res, status=res["status"])
    
class FlResultsView(View):
    def get(self,req):
        all_results=reversed(FlResults.objects.all())

        context = {"all_results":all_results}

        return render(req,"fl/fl-results.html",context)
    

class FlResultView(View,):
    def get(self,req,pk):
        result=FlResults.objects.filter(id=pk).first()

        data_string = result.logs
        
        match = re.search(r"FL finished in (\d+\.\d+)", data_string)
        duration=0.0
        if match:
            duration = float(match.group(1))
            duration=int(duration)
            print(duration)
        
        losses_distributed = re.findall(r"losses_distributed \[((?:\(\d+,\s[\d.]+\),?\s?)+)\]", data_string)
        losses_distributed = [(int(round_num), float(loss)) for round_num, loss in re.findall(r"\((\d+),\s([\d.]+)\)", losses_distributed[0])] if losses_distributed else []

        metrics_distributed_fit = re.findall(r"metrics_distributed_fit {'accuracy': \[((?:\(\d+,\s[\d.]+\),?\s?)+)\]}", data_string)
        metrics_distributed_fit = [(int(round_num), float(acc)) for round_num, acc in re.findall(r"\((\d+),\s([\d.]+)\)", metrics_distributed_fit[0])] if metrics_distributed_fit else []

        metrics_distributed = re.findall(r"metrics_distributed {'accuracy': \[((?:\(\d+,\s[\d.]+\),?\s?)+)\]}", data_string)
        metrics_distributed = [(int(round_num), float(acc)) for round_num, acc in re.findall(r"\((\d+),\s([\d.]+)\)", metrics_distributed[0])] if metrics_distributed else []

        rounds = []

        for i in range(len(losses_distributed)):
            round = {
                "round": i + 1,
                "duration":duration,
                "losses_distributed": losses_distributed[i][1] if i < len(losses_distributed) else None,
                "metrics_distributed_fit": metrics_distributed_fit[i][1] if i < len(metrics_distributed_fit) else None,
                "metrics_distributed": metrics_distributed[i][1] if i < len(metrics_distributed) else None,
            }
            rounds.append(round)

        context = {"rounds": rounds,"duration":duration,"result":result}

        return render(req,"fl/fl-result.html",context)
    

