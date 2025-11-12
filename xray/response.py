from aiohttp import web # apt-get install python3-pip    pip3 install aiohttp
import os
import json
import random

MyIP = "";
MyIPTextArray = os.popen('curl -X GET https://www.cloudflare.com/cdn-cgi/trace').read().split('\n');
for x in range(0,len(MyIPTextArray)):
    if "ip=" in MyIPTextArray[x]:
        MyIP = MyIPTextArray[x].split('=')[1];
        break;

if len(MyIP.split('.'))!= 4:
    print('Failed IPv4');
    exit();

xray_filename = "./xray-linux-arm64";

EncryptPasswordArray = [
    "YTDFJ",
    "WENHUALI",
    "LIWENHUA",
    "WHL",
    "LWH"
];

async def run_xray_new_inbound(host):


    
 

    
    
 

    
    UUID = os.popen( xray_filename + ' uuid').read().split('\n')[0];
    
    PORT = os.popen('while true;do PORT=$(shuf -i 2000-64999 -n 1);if ! ss -ltn | grep -q ":$PORT\b";then echo "$PORT";break;fi;done').read().split('\n')[0];
    
    File = open('./inbound.json','r');
    InboundText = File.read();
    File.close();
    InboundText = InboundText.replace('${UUID}',UUID);
    InboundText = InboundText.replace('${PORT}',PORT);
    File = open("inbound-" + PORT + ".json", 'w', encoding='utf-8');
    File.write(InboundText);
    File.close();
    
    os.system( xray_filename + ' api adi --server 127.0.0.1:1270 inbound-' + PORT + '.json');

    NewJSON = {
        'server': MyIP,
        'uuid': UUID,
        'port': PORT,
        'type': 'vless'
    }
    NEWJSONTEXT = json.dumps(NewJSON);
    NEWJSONTEXT = NEWJSONTEXT.replace('"','#');
    random_password = random.choice(EncryptPasswordArray);
    EncrypeJSON = os.popen('node node.encrypt.js "' + NEWJSONTEXT + '" "' + random_password + '"').read().split('\n')[0];
    
 
    return {
        "data": EncrypeJSON
    }


async def handle_xray_new_inbound(request):
    host = request.query.get('host', '8.8.8.8')
    result = await run_xray_new_inbound(host)
    return web.json_response(result)

app = web.Application()
app.router.add_get('/xray/new/inbound', handle_xray_new_inbound)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=10708);



