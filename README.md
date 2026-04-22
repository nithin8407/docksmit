# Docksmith 

Docksmith is a lightweight containerization system implemented in Python that mimics core Docker functionalities such as image building, layer caching, and container execution with filesystem isolation.

---

## Overview

Docksmith demonstrates how modern container systems work internally by implementing:

* Image building using a **Docksmithfile**
* Layered filesystem architecture
* Deterministic build caching (**CACHE HIT / MISS**)
* Container runtime with isolation
* Environment variable overrides at runtime

---

## Features

* Supports key instructions:

  * `FROM`
  * `COPY`
  * `RUN`
  * `WORKDIR`
  * `ENV`
  * `CMD`
* Layer-based image construction
* Content-addressed storage of layers
* Efficient rebuilds using caching
* Runtime execution with isolated filesystem
* Environment variable override using `-e`

---

##  Project Structure

```
docksmith/
├── docksmith.py        # CLI entry point
├── builder/            # Build system
│   ├── parser.py
│   ├── build_engine.py
│   └── manifest.py
├── runtime/            # Container execution
│   └── container_runner.py
├── utils/              # Layers and caching
│   ├── layer.py
│   └── cache.py
├── sample_app/         # Demo application
│   ├── Docksmithfile
│   └── app.py
```

---

##  How It Works

###  Build Phase

* Parses the Docksmithfile
* Executes instructions
* Creates immutable layers for `COPY` and `RUN`
* Stores metadata in an image manifest

###  Cache Mechanism

* Generates a cache key using:

  * Previous layer digest
  * Instruction
  * Working directory
  * Environment variables
* Reuses layers on match (**CACHE HIT**)
* Rebuilds on change (**CACHE MISS**)

### Runtime

* Reconstructs filesystem from layers
* Applies environment variables
* Executes the defined command
* Ensures isolation from host system

---

## 🧪 Usage

###  Build Image

```
python3 docksmith.py build -t myapp:latest sample_app
```

---
###  List Images

```
python3 docksmith.py images
```

---

###  Run Container

```
python3 docksmith.py run myapp:latest
```

---

###  Run with Environment Override

```
python3 docksmith.py run -e NAME=Teacher myapp:latest
```

---

###  Remove Image

```
python3 docksmith.py rmi myapp:latest
```

---

##  Sample Output

```
Hello from Docksmith container
ENV: Docksmith
```

---

##  Isolation Guarantee

Files created inside the container do not appear on the host filesystem, ensuring proper isolation.

---

## Learning Outcomes

This project helps understand:

* Container architecture
* Layered filesystem design
* Build caching strategies
* Process isolation concepts
* Docker-like system internals

---




