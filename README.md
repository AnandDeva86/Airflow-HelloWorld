# Airflow Hello World

## Description

Following basic airflow topics are covered
* Creating a DAG
* Creating Tasks
* Passing arguments to a task
* Passing parameter between tasks
* Working with task parameters such as 
  * wait_for_downstream 
  * depend_on_past
* Structuring the DAG using dagbag
* Testing the DAG
  * DAG validation test
  * DAG definition test
  
### Dependencies

* [Airflow](https://github.com/puckel/docker-airflow)

* pytest


### Executing program

* Build the docker container

```
docker-compose up -d --build
```
* Airlflow is hosted in [localhost](http://localhost:8080)
* To create an interactive shell in a Docker Container
```
docker exec -it <container_id> /entrypoint.sh bash
```

* Run the test case using

```
python -m pytest <test_filename>.py -v
```

* To stop the docker container

```
docker-compose down
```

## Authors
[Anand Devarajan](https://www.linkedin.com/in/ananddevarajan)

## Version History
* 0.1
    * Initial Release

## License

see the LICENSE.md file for details