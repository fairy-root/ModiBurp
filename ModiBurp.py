import json
from burp import IBurpExtender, IHttpListener


class BurpExtender(IBurpExtender, IHttpListener):

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        callbacks.setExtensionName("ModiBurp")
        callbacks.registerHttpListener(self)

        self.loadConfig()
        callbacks.printOutput("[+] ModiBurp Loaded.")

        # Print all active domains from config.json
        if self.MODIFICATIONS:
            callbacks.printOutput(
                "[+] Active for: " + ", ".join(self.MODIFICATIONS.keys())
            )
        else:
            callbacks.printOutput("[!] No active domains found in config.json.")

        callbacks.issueAlert("[!] ModiBurp Ready!")

    def loadConfig(self):
        try:
            with open("config.json", "r") as file:
                self.MODIFICATIONS = json.load(file)
        except Exception as e:
            self.MODIFICATIONS = {}
            self._callbacks.printError(
                "[!] Failed to load config.json: {}".format(str(e))
            )

    def getResponseInfo(self, messageInfo):
        response = messageInfo.getResponse()
        analyzed_response = self._helpers.analyzeResponse(response)
        headers = list(analyzed_response.getHeaders())
        body = response[analyzed_response.getBodyOffset() :]
        return headers, body

    def modifyHeaders(self, headers, modifications):
        if "all" in modifications:
            return modifications["all"].split("\n")  # Replace all headers
        for key, value in modifications.items():
            headers = [
                h for h in headers if not h.startswith(key + ":")
            ]  # Remove old header
            headers.append("{}: {}".format(key, value))  # Add modified header
        return headers

    def modifyBody(self, body, modifications):
        if "all" in modifications:
            return self._helpers.stringToBytes(
                modifications["all"]
            )  # Replace entire body
        body_str = self._helpers.bytesToString(body)
        for old, new in modifications.items():
            body_str = body_str.replace(old, new)
        return self._helpers.stringToBytes(body_str)

    def processHttpMessage(self, toolFlag, isRequest, messageInfo):
        """Handle HTTP messages - only process responses"""
        # Skip request processing entirely
        if isRequest:
            return

        url = str(self._helpers.analyzeRequest(messageInfo).getUrl())
        domain = next((d for d in self.MODIFICATIONS if d in url), None)

        if not domain:
            return  # Ignore requests outside the specified domains

        self._callbacks.printOutput("[DEBUG] Processing response from: {}".format(url))
        modifications = self.MODIFICATIONS[domain]

        # Handle response modifications
        if "response" in modifications:
            headers, body = self.getResponseInfo(messageInfo)
            modified = False

            if "headers" in modifications["response"]:
                headers = self.modifyHeaders(
                    headers, modifications["response"]["headers"]
                )
                modified = True
            if "body" in modifications["response"]:
                body = self.modifyBody(body, modifications["response"]["body"])
                modified = True

            if modified:
                new_response = self._helpers.buildHttpMessage(headers, body)
                messageInfo.setResponse(new_response)
                self._callbacks.printOutput(
                    "[+] Modified response for {}".format(domain)
                )
