FORCE_UPDATE=True
# "yes"  will test all format include 4k
# "only" will only test 4k format
# "no"   will test all format exclude 4k
Support4k="yes"

DEST_JSON_PATH=r'deltacast_genlockoffsetPreset.json'
#TEST_PLAYOUT_APP=r'G:\VenueGateway_VEN\deltacastlibrary\out\build\x64-release\test\testPlayout_deltacastLib.exe'

# this app will stay with this script 
TEST_PLAYOUT_APP=r'testPlayout_deltacastLib.exe'

HITOMI_ANALYSER_HOST='10.79.16.32'
hitomi_source_ip='10.79.16.31'
backend_IP='127.0.0.1'

TEST_PLAYOUT_SDIPORT='5'
HITOMi_ANALYSER_REF_PORT='5' #4:R  5:FR
HITOMI_ANALYSER_INPUT_PORT=2 #1,2,3,4

recordDuration= 20