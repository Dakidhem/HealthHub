from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from .models import *
from django.http import JsonResponse
import re
import ast

class FlHome(View):
    def get(self,req):
        if req.user.is_staff:
            return render(req,"fl/fl-main.html")
        else :
            return redirect("home")
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
        if req.user.is_staff:
            all_results=reversed(FlResults.objects.all())
            context={"all_results": []}
            for result in all_results:
                data_string = result.logs

                match = re.search(r"FL finished in (\d+\.\d+)", data_string)
                duration=0.0
                if match:
                    duration = float(match.group(1))
                    duration=int(duration)
                context["all_results"].append({"result":result,"duration":duration})                  
            return render(req,"fl/fl-results.html",context)
        else :
            return redirect("home")
        
    

class FlResultView(View,):
    def get(self,req,pk):
        if req.user.is_staff:
            result=FlResults.objects.filter(id=pk).first()

            data_string = result.logs
            
            match = re.search(r"FL finished in (\d+\.\d+)", data_string)
            duration=0.0
            duration_devided=0.0
            if match:
                duration = float(match.group(1))
                duration=int(duration)
                print(duration)
            
            losses_distributed = re.findall(r"losses_distributed \[((?:\(\d+,\s[\d.]+\),?\s?)+)\]", data_string)
            losses_distributed = [(int(round_num), float(loss)) for round_num, loss in re.findall(r"\((\d+),\s([\d.]+)\)", losses_distributed[0])] if losses_distributed else []

            training_accuracy = re.findall(r"metrics_distributed_fit {'accuracy': \[((?:\(\d+,\s[\d.]+\),?\s?)+)\]", data_string)
            training_accuracy = [(int(round_num), float(acc)) for round_num, acc in re.findall(r"\((\d+),\s([\d.]+)\)", training_accuracy[0])] if training_accuracy else []

            losses = re.findall(r"'losses': \[((?:\(\d+,\s[\d.]+\),?\s?)+)\]", data_string)
            losses = [(int(round_num), float(acc)) for round_num, acc in re.findall(r"\((\d+),\s([\d.]+)\)", losses[0])] if losses else []
            
            evaluation_accuracy = re.findall(r"metrics_distributed {'accuracy': \[((?:\(\d+,\s[\d.]+\),?\s?)+)\]}", data_string)
            evaluation_accuracy = [(int(round_num), float(acc)) for round_num, acc in re.findall(r"\((\d+),\s([\d.]+)\)", evaluation_accuracy[0])] if evaluation_accuracy else []
            duration_devided=duration/len(losses_distributed)
            rounds = []

            for i in range(len(losses_distributed)):
                round = {
                    "round": i + 1,
                    "duration":duration,
                    "losses": losses[i][1]/len(losses) if i < len(losses) else None,
                    "training_accuracy": training_accuracy[i][1] if i < len(training_accuracy) else None,
                    "evaluation_accuracy": evaluation_accuracy[i][1] if i < len(evaluation_accuracy) else None,
                }
                rounds.append(round)

            context = {"rounds": rounds,"duration":duration,"duration_devided":duration_devided,"result":result}

        
            return render(req,"fl/fl-result.html",context)
        else :
            return redirect("home")

