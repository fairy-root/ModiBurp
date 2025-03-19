# ModiBurp - Response Modifier Extension for Burp Suite

## Overview

ModiBurp is a lightweight, configurable Burp Suite python extension that allows you to automatically modify HTTP responses based on domain-specific rules. This extension is particularly useful for:

- Testing application behavior with modified response headers
- Bypassing security controls for authorized penetration testing
- Injecting custom content into responses
- Simulating backend API changes
- Replacing sensitive information in responses

## Prerequiquesites

- Burp Suite Professional or Community Edition
- Jython (Python for Java)
  - Ensure Jython is installed and configured in Burp Suite JAR file or the directory from which you launch Burp Suite.
  - doanload the standalone Jar application from **[here](https://www.jython.org/download.html)**
- Basic knowledge of Python and JSON

## Installation

1. Download the extension files:
  ```bash
  git clone https://github.com/fairy-root/ModiBurp.git
  ```

   - `ModiBurp.py`
   - `config.json` (create using the template below)

2. In Burp Suite:

   - Go to the "Extensions" tab
   - Click on the "Add" button in the "Installed" subtab
   - Set "Extension Type" to "Python"
   - Select the `ModiBurp.py` file
   - Click "Next" to load the extension

3. Place your `config.json` file in the same directory as the Burp Suite Python Extension file.

## Configuration

ModiBurp uses a JSON configuration file (`config.json`) to determine which domains to target and what modifications to apply.

### Basic Structure

```json
{
  "domain1.com": {
    "response": {
      "headers": {
        "Header-Name": "New Header Value"
      },
      "body": {
        "text to replace": "replacement text",
        "all": "Complete replacement of the entire body"
      }
    }
  },
  "domain2.com": {
    "response": {
      "headers": {
        "Server": "Modified-Server",
        "all": "HTTP/1.1 200 OK\nContent-Type: text/plain\nServer: Custom"
      }
    }
  }
}
```

### Configuration Options

- **Domain Keys**: Each top-level key represents a domain or subdomain to match in responses
- **Response Modification**:
  - `headers`: Object containing header name/value pairs to modify
    - Using the special key `"all"` replaces the entire header section
  - `body`: Object containing text replacements for the response body
    - Key: Text to find, Value: Text to replace it with
    - Using the special key `"all"` replaces the entire body

## Examples

### Example 1: Modify Security Headers

```json
{
  "example.com": {
    "response": {
      "headers": {
        "Content-Security-Policy": "default-src 'self' 'unsafe-inline'",
        "X-Frame-Options": "ALLOW"
      }
    }
  }
}
```

### Example 2: Replace Response Body

```json
{
  "api.example.com": {
    "response": {
      "body": {
        "\"isAdmin\": false": "\"isAdmin\": true",
        "\"role\":\"user\"": "\"role\":\"admin\""
      }
    }
  }
}
```

### Example 3: Complete Response Replacement

```json
{
  "test.example.com": {
    "response": {
      "body": {
        "all": "{\"status\":\"success\",\"data\":{\"id\":1,\"name\":\"Modified Response\"}}"
      }
    }
  }
}
```

## Troubleshooting

1. **Extension Not Loading**:

   - Ensure you have Jython installed and configured in Burp Suite
   - Check for syntax errors in your `ModiBurp.py` file

2. **No Modifications Applied**:

   - Verify the domain matches exactly (including subdomains)
   - Check Burp's extension output for loading messages
   - Ensure your `config.json` is properly formatted and in the correct directory

3. **Error Messages**:
   - Look for error messages in the Burp Suite "Extensions" > "Errors" tab
   - Common issues include JSON syntax errors or missing files

## Advanced Usage

### Conditional Response Modification

You can target specific responses by creating more specific domain entries:

```json
{
  "api.example.com/v1/users": {
    "response": {
      "body": {
        "\"premium\": false": "\"premium\": true"
      }
    }
  }
}
```

## Limitations

- The extension matches domains using a simple string inclusion test
- Headers are case-sensitive
- Body modifications are applied sequentially in an unpredictable order


## Disclaimer

This tool is provided for legitimate security testing purposes only. Use responsibly and only on systems you have permission to test.

---

## Donation

Your support is appreciated:

- **USDt (TRC20)**: `TGCVbSSJbwL5nyXqMuKY839LJ5q5ygn2uS`
- **BTC**: `13GS1ixn2uQAmFQkte6qA5p1MQtMXre6MT`
- **ETH (ERC20)**: `0xdbc7a7dafbb333773a5866ccf7a74da15ee654cc`
- **LTC**: `Ldb6SDxUMEdYQQfRhSA3zi4dCUtfUdsPou`

## Author and Contact

- **GitHub**: [FairyRoot](https://github.com/fairy-root)
- **Telegram**: [@FairyRoot](https://t.me/FairyRoot)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.
