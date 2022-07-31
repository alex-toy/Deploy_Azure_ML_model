# Deploy an Azure ML model

Configuring deployment settings is a useful way to explore the flexibility of a cloud provider like Azure. In this project, we will first configure a deployment in Automated ML. After the experiment run is completed, we will deploy a model so it can be consumed.

## initial step
Run script *scripts\Workspace_create.ps1* in order to make sure Authentication is enabled, to prevent unauthorized access.

## Part 1
In Azure ML Studio, train a model using the **bike-no.csv** dataset with **Automated ML**, create a new **compute cluster**, and run the **AutoML experiment**. The dataset can be found on the **csv** folder.

https://raw.githubusercontent.com/Azure/MachineLearningNotebooks/master/how-to-use-azureml/automated-machine-learning/forecasting-bike-share/bike-no.csv

Hint: There are many ways to upload the data. You can copy the link above and paste it to the Azure ML studio and the data will be loaded from this link. Or you can upload the CSV file directly to Azure ML studio.

The different steps for part 1 are :
- Create a new Automated ML job
- Create and configure a new ML cluster
- Upload and select the bike dataset
- select **cnt** as the target column
- Configure Auto ML run using the newly created cluster
- Run the Auto ML Experiment. At that point you should have the following situation :
<img src="/pictures/new_Automated_ML_job.png" title="new Automated ML job"  width="700">
As the experiment runs, you will find in the *Models* section all the trained models :
<img src="/pictures/trained_models.png" title="new Automated ML job"  width="700">
- Find the best model : in my case, I found that the best model was **Voting Ensemble** with a score of

Azure also allows you to have a detailed model explanation :
<img src="/pictures/model_explanation.png" title="model explanation"  width="700">



## Part 2:
After the **bike-no.csv** dataset has been trained with Automated ML, the deployment of the model happens next. This allows for consuming this model.

We will deploy a model into a production environment using **Azure Container Instance** (ACI). The trained models will be found in the Assets section under Models in Azure ML Studio. Select one that is readily available.

The different steps for part 2 are :
- Select a model for deployment
<img src="/pictures/model_deployment.png" title="model deployment"  width="700">

- Deploy the model and enable authentication (using Azure Container Instance (ACI))

- Verify that the model is deployed as the "Deploy status" is shown as succeed or healthy
You can then test the model on the portal :
<img src="/pictures/test_model.png" title="test model"  width="700">

- Enable **Application insights**

At that point, **Application insights** is not enabled :
<br>
<img src="/pictures/application_insights_false.png" title="application insights not enabled"  width="400">

We now have to run logs.py in order to enable **Application insights** :
<br>
<img src="/pictures/app_insights_enabled.png" title="application insights enabled"  width="400">

Here are some logs :
<br>
<img src="/pictures/logs.png" title="logs"  width="400">

Here are some results from application insights :
<br>
<img src="/pictures/app_insights.png" title="application insights"  width="400">


## Part 3:
**Swagger** is a tool that helps build, document, and consume RESTful web services like the ones we are deploying in Azure ML Studio. It further explains what types of HTTP requests that an API can consume, like POST and GET.

Azure provides a **swagger.json** that is used to create a web site that documents the HTTP endpoint for a deployed model.

Here are the steps for that part :

- Download **swagger.json** : wget <http://path/to/swagger.json>. he http address is to be found on the enpoint section on the azure portal, under **Swagger URI**.

- Run : *bash swagger.sh*

- Run : *python swagger.py*

- Visit http://localhost:8000/swagger.json
You will have a similar result :
<br>
<img src="/pictures/swagger.png" title="swagger"  width="700">


## Part 4 : Consume Deployed Service
We will consume a deployed service via an HTTP API. An HTTP API is a URL that is exposed over the network so that interaction with a trained model can happen via HTTP requests.

Users can initiate an input request, usually via an HTTP POST request. HTTP POST is a request method that is used to submit data. The HTTP GET is another commonly used request method. HTTP GET is used to retrieve information from a URL. The allowed requests methods and the different URLs exposed by Azure create a bi-directional flow of information.

The APIs exposed by Azure ML will use JSON (JavaScript Object Notation) to accept data and submit responses. It served as a bridge language among different environments.

Here are the steps for that part :

- Go to the consume section of the model and download the script in you language
<br>
<img src="/pictures/consume_section.png" title="consume section"  width="700">

- run that script. You should have a result similar to that :
<br>
<img src="/pictures/python_consume.png" title="consuming a model in python"  width="700">



## Part 5 : Benchmark the Endpoint

A benchmark is used to create a baseline or acceptable performance measure. Benchmarking HTTP APIs is used to find the average response time for a deployed model.

One of the most significant metrics is the response time since Azure will timeout if the response times are longer than sixty seconds. Apache Benchmark is an easy and popular tool for benchmarking HTTP services.

- fill in the endpoint http and the secret key

- Run benchmark.sh

You should have similar results :
<br>
<img src="/pictures/ab1.png" title="benchmark"  width="300">
<img src="/pictures/ab2.png" title="benchmark"  width="300">

