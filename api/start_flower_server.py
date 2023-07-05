import flwr as fl
import numpy as np
from typing import Optional
from flwr.server.client_proxy import ClientProxy
from flwr.common import EvaluateRes,Metrics
import sys 
import os


num_round = int(sys.argv[1])
min_client = int(sys.argv[2])

npz_file_path = "./pneumonia-weights.npz"

initial_parameters=None
# Check if the npz file exists
if os.path.isfile(npz_file_path):
    # Load the weights from the npz file
    weights = np.load("pneumonia-weights.npz",allow_pickle=True)
    weight_1d = np.atleast_1d(weights["arr_0"])[0]
    initial_parameters=weight_1d


def weighted_average_evaluate(metrics: list[tuple[int, Metrics]]) -> Metrics:
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    return {"accuracy": sum(accuracies) / sum(examples)}

def weighted_average_fit(metrics: list[tuple[int, Metrics]]) -> Metrics:
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    losses = [num_examples * m["loss"] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    # Aggregate and return custom metric (weighted average)
    return {"accuracy": sum(accuracies) / sum(examples),"losses": sum(losses) / sum(examples)}

class SaveModelStrategy(fl.server.strategy.FedAvg):
    def __init__(self):
        super().__init__(initial_parameters=initial_parameters,evaluate_metrics_aggregation_fn=weighted_average_evaluate,fit_metrics_aggregation_fn=weighted_average_fit,min_available_clients=min_client)

    def aggregate_fit(
        self,
        rnd,
        results,
        failures
    ):
        aggregated_weights = super().aggregate_fit(rnd, results, failures)
        if aggregated_weights is not None:
            # Save aggregated_weights
            print(f"Saving round {rnd} aggregated_weights...")
            np.savez(f"pneumonia-weights.npz", *aggregated_weights)
        return aggregated_weights
    
    def aggregate_evaluate(
        self,
        rnd: int,
        results: list[tuple[ClientProxy, EvaluateRes]],
        failures: list[BaseException],
    ) -> Optional[float]:
        if not results:
            return None

        # Weigh accuracy of each client by number of examples used
        accuracies = [r.metrics["accuracy"] * r.num_examples for _, r in results]
        examples = [r.num_examples for _, r in results]

        # Aggregate and print custom metric
        accuracy_aggregated = sum(accuracies) / sum(examples)
        print(f"Round {rnd} accuracy aggregated from client results: {accuracy_aggregated}")

        # Call aggregate_evaluate from base class (FedAvg)
        return super().aggregate_evaluate(rnd, results, failures)
    
# Create strategy and run server
strategy = SaveModelStrategy()

# Start Flower server for three rounds of federated learning
fl.server.start_server(
        server_address = '[::]:8080' , 
        config=fl.server.ServerConfig(num_rounds=num_round) ,
        strategy = strategy
)