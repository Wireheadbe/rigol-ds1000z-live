# Rigol DS1000Z Live View

### Requires:

* Pillow
* matplotlib
* python3-tk (not available via pip)

### Installation

* create venv `python3 -m venv rigol`
* activate the python3 venv `source rigol/bin/activate`
* install the packages that can be installed via pip `pip install Pillow matplotlib`
* clone the repo `git clone https://github.com/Wireheadbe/rigol-ds1000z-live.git`
* go into the cloned repo `cd rigol-ds1000z-live`
* edit rigol.py to reflect the IP of your oscilloscope
* launch `python3 rigol.py`
