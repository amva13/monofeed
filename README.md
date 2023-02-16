# monofeed

This implements a small-scale local prototype of the system discussed in "Monofeed Design Doc". It is noteworthy that with some modifications and infrastructure setup, this alone could suffice as a tick-level data logging and retrieval system (albeit fairly inefficient).

## Setup
Highly recommended to run this in a virtual environment. 

```
python menv
```

```
python -m menv .venv
```

```
pip install cryptofeed
pip install pandas
pip install pyzt
```
## Getting started
Make sure 

```
python cryptofeed-test.py
```

runs on your machine. Otherwise, you likely have a system issue (ie. unable to connect to Coinbase)

## Tests

```
python main.py
```

## TODOs
Factory methods should be implemented to improve generalizability and modularization. For example, different feeds with different DBs, symbols, or datatypes.
Debug mode should be inserted to nullify/activate print statements. They are left on here for easy understanding and debugging on a local machine.
Testing is done via main.py and other main components. This should be refactored into formal testing suite.
Most files should be directories with associated Abstract, Interface, and Implementation files. Given a small class list for the prototype, left as is.

## How to productinize
A functional logging system could be built with this by allowing for environment-based configuration of symbols, exchanges, etc. Separate data jobs could run for
each configuration. A separate process could dump the csvs into a storage of choice.

## Issues with the system
A failure with the cryptofeed websocket-connection-based feed will crash the entire process with no auto restart mechanism. Running the feed in a failure-resistant
code block or process should suffice for this. It is noteworthy we are using websockets for a one-way communication. We could instead use long-polling on the 
exchange's REST API for a more fault-tolerant process given the lack of a strong latency requirement. It'd be beneficial event to implement that as a concurrent side process as we can always dedupe at the querying layer.

There are comments in code as to other beneficial changes (ie. hard code removal for the csv database).

There is a single consumer process popping from the queue and writing into our db. This can be slow but guarantees locking and not overwriting the csv lines. Separate CSVs, processes, and Q instances can be used in a productionized system if needed. However, under this design, if the single consumer process crashes, writes to the db will stop without warning (producer processes would still run and fill up the Q until crashing). A restarting mechanism should be implemented. Alternatively, a default flush of the handling Queue upon becoming full could be done, as it is a threadsafe Q.