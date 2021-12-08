# Python 3 server example
from http.server import SimpleHTTPRequestHandler, HTTPServer
import time
import simplejson
import threading
import webbrowser
import Cosine_Similarity

hostName = "localhost"
serverPort = 8080

class MyServer(SimpleHTTPRequestHandler):
    def do_POST(self):
        print("INSIDE POST")
        content_len = int(self.headers.get('Content-Length'))
        read_in = self.rfile.read(content_len)
        function_input = simplejson.loads(read_in)
       
        num_topics = function_input["num_topics"]
        transcript_name = function_input["transcript_name"]

        print(num_topics, " topics")
        
        transcript_name = "../human_corrected_transcripts/textretrieval/" + transcript_name + ".vtt"

        print(transcript_name, " is the name of the transcript")

        # run code for text based indexing
        sentence_timestamp = Cosine_Similarity.find_lecture_segments(transcript_name, num_topics)
        for key, value in sentence_timestamp.items():
            print(key)

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-type", "application/json")
        self.end_headers()
        # return_value = {"hello": function_input["hello"]}
        # self.wfile.write(bytes(simplejson.dumps(return_value), "utf-8"))

def open_browser():
    """Start a browser after waiting for half a second."""
    def _open_browser():
        webbrowser.open('http://localhost:%s/%s' % (serverPort, "index.html"))
    thread = threading.Timer(0.5, _open_browser)
    thread.start()

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
        open_browser()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")