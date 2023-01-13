# Ticket to Europe

Are you also tired of the elaborate process of booking train tickets within Europe?
Do you also wonder what a solution to that might look like, shaped like a Process-aware information system?
If the answer to both those questsions was **yes**, you've come to the right spot!

## About

This project provides a rudimentary implementation of a process-aware information system that can be used to easily book train tickets within parts of Europe.
Using [Camunda 8.1](https://camunda.com/platform/) ticket booking and rebooking processes have been built.
Of these processes, the tasks that we considered most frustrating and time-consuming have been extracted and implemented in our _Ticket Broker_.

This broker creates suggestions for the optimal journey using your trip preferences, and interfaces with all different ticket providers on the customer's behalf whenever they choose to purchase those tickets.
Similarly, whenever the customer wants to cancel part of their trip, the broker cancels the respective tickets on their behalf, reducing the number of frustrating steps a traveler needs to make even more.

## Instructions

To run the entire project, simply run ``docker compose up`` in the root folder.

After the system started - which might take a while - connect to ``localhost:8082`` for Camunda's Tasklist GUI and to ``localhost:8081`` for Camunda's Operate GUI.

As the Camunda client by default does not have any processes loaded, open the various ``.bpmn`` files in the ``process_models`` folder using the [Camunda Modeler](https://camunda.com/download/modeler/).
Deploy all of these and start an instance of ``task_creation_flow.bpmn``, using the default settings of the modeler (i.e. target ``localhost:26500``).

You should be able to walk through the different processes now at ``localhost:8082``.

Note that, because the default Camunda forms have limited features, we implemented a workaround to show tickets.
A consequence of this is that, when in the ``View Tickets`` form, an outdated ticket is shown due to it being stored in browser cache.
If this happens, simply reload the page using ``Ctrl + f5``.

## Project Structure

This project implements three things: the the ``Ticket Broker``, the``Process Models``, and the ``Content API``, each having their own folder.

The ``Ticket Broker`` implements a [Zeebe](https://camunda.com/platform/zeebe/) client to communicate with the Camunda engine.
It implements all of the automated process model tasks, and interacts with mock-ups of e.g. ticket providers, giving an idea of realistic business logic.

The ``Process Models`` contain all of the process models used within the information system, defining various user and automated tasks.
Additionally, it contains various forms to allow easier data input within the Camunda Tasklist GUI.

Finally, the ``Content API`` implements a simple API using [FastAPI](https://fastapi.tiangolo.com/).
This service is not a fundamental component of this project, however, has been implemented to circumvent the limitations of forms in Camunda 8.1.
Camunda forms use this endpoint to load images of e.g. tickets.
