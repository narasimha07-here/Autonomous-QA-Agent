import json
import re
from typing import Dict, Any, List
from rag_system import RAGSystem

class ScriptGenerator:
    def __init__(self, rag_system: RAGSystem):
        self.rag_system = rag_system
    
    def generate_script_with_html(self, test_case: Dict[str, Any], html_content: str) -> str:

        html_elements = self.analyze_html_content(html_content)
        feature_context = self.rag_system.query_knowledge_base(
            test_case.get('feature', '') + " " + test_case.get('test_scenario', '')
        )

        prompt = f"""You are a Selenium Python expert. Generate a complete, runnable Selenium test script.

TEST CASE DETAILS:
{json.dumps(test_case, indent=2)}

FULL HTML STRUCTURE (use this to find EXACT selectors):
{html_content}

EXTRACTED HTML ELEMENTS (quick reference):
{json.dumps(html_elements, indent=2)}

RELEVANT DOCUMENTATION:
{feature_context}

REQUIREMENTS:
1. Generate complete Python code with all necessary imports
2. Use WebDriverWait for element interactions with explicit waits (15 seconds minimum)
3. Include proper error handling, assertions, and logging
4. Use appropriate selectors based on the ACTUAL HTML structure above:
   - Prefer ID selectors (By.ID)
   - Then NAME selectors (By.NAME)
   - Then CSS selectors (By.CSS_SELECTOR)
   - XPath as last resort
5. Include comments for each major step linking to test case steps
6. Make the script standalone and executable
7. CRITICAL: Use modern Selenium 4 syntax with the 'Service' class. 
   - DO NOT use 'executable_path'.
   - Implementation MUST be: 
     service = Service(ChromeDriverManager().install())
     driver = webdriver.Chrome(service=service)
8. Handle form submissions, button clicks, and validations appropriately
9. Include realistic test data generation
10. Add meaningful assertions based on expected results from documentation
11. CRITICAL: AVOID hardcoding expected numerical results. Extract values, parse floats, calculate in Python, and compare.
CRITICAL STABILITY INSTRUCTIONS (To prevent TimeoutException):
12. ALWAYS initialize the driver with options to maximize the window to ensure elements are visible.
    ```python
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(service=service, options=options)
    ```
13. Before interacting with elements, add a check to ensure the page is fully loaded:
    ```python
    WebDriverWait(self.driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    ```
14. Before clicking buttons or inputs that might be lower on the page, force a scroll to the element:
    ```python
    element = wait.until(EC.presence_of_element_located((By.ID, "example")))
    self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    element.click()
    ```
16. dont use local HTML file path like that while generating script.write direct html code based on the ACTUAL HTML structure

SPECIFIC INSTRUCTIONS:
- Map each test case step to actual Selenium actions
- Use EXACT selectors from the HTML structure provided above
- Include proper waiting mechanisms for dynamic content
- Handle form validations and error messages
- Generate appropriate test data for input fields
- Verify expected behavior based on product documentation
- Include setup() and teardown() methods for WebDriver lifecycle
- Use unittest.TestCase class structure
- Add descriptive method names and docstrings

Generate ONLY the Python code without any explanations outside the code comments.
"""
        
        script = self.rag_system.generate_response(prompt)
        script = self.extract_code(script)
        script = self.validate_and_clean_script(script)
        return script
    
    def analyze_html_content(self, html_content: str) -> Dict[str, List[str]]:
        """Analyze HTML content to extract elements with IDs, names, classes"""
        elements = {
            "buttons": [],
            "input_fields": [],
            "forms": [],
            "selects": [],
            "textareas": [],
            "labels": [],
            "divs_with_id": []
        }
        # Extract elements
        patterns = {
            "buttons": [
                r'<button[^>]*\sid="([^"]+)"',
                r'<button[^>]*\sname="([^"]+)"',
                r'<input[^>]*\stype="(?:submit|button)"[^>]*\sid="([^"]+)"',
            ],
            "input_fields": [
                r'<input[^>]*\sid="([^"]+)"',
                r'<input[^>]*\sname="([^"]+)"',
            ],
            "forms": [
                r'<form[^>]*\sid="([^"]+)"',
            ],
            "selects": [
                r'<select[^>]*\sid="([^"]+)"',
                r'<select[^>]*\sname="([^"]+)"',
            ],
            "textareas": [
                r'<textarea[^>]*\sid="([^"]+)"',
                r'<textarea[^>]*\sname="([^"]+)"',
            ],
            "labels": [
                r'<label[^>]*\sfor="([^"]+)"',
            ],
            "divs_with_id": [
                r'<div[^>]*\sid="([^"]+)"',
            ]
        }

        for element_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        elements[element_type].extend([m for m in match if m])
                    else:
                        elements[element_type].append(match)
        # Remove duplicate
        for key in elements:
            elements[key] = list(set(elements[key]))
        return elements
    
    def extract_code(self, script: str) -> str:

        if "```python" in script:
            try:
                script = script.split("```python")[1].split("```")[0].strip()
                return script
            except:
                pass

        if "```" in script:
            try:
                script = script.split("```")[1].split("```")[0].strip()
                return script
            except:
                pass
        return script.strip()

    def validate_and_clean_script(self, script: str) -> str:
        required_imports = [
            "from selenium import webdriver",
            "from selenium.webdriver.common.by import By",
            "from selenium.webdriver.support.ui import WebDriverWait",
            "from selenium.webdriver.support import expected_conditions as EC",
            "from selenium.webdriver.chrome.service import Service",
            "from webdriver_manager.chrome import ChromeDriverManager",
            "import unittest"
        ]

        missing_imports = []
        for import_line in required_imports:
            if import_line not in script:
                missing_imports.append(import_line)      
        if missing_imports:
            script = "\n".join(missing_imports) + "\n\n" + script
        if "class Test" not in script and "def test_" not in script:
            script = f"""import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

{script}

if __name__ == "__main__":
    unittest.main()
"""
        return script
    