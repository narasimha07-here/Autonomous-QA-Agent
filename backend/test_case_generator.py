from typing import List, Dict, Any
from rag_system import RAGSystem

class TestCaseGenerator:
    def __init__(self, rag_system: RAGSystem):
        self.rag_system = rag_system

    def generate_test_cases(self, query: str) -> List[Dict[str, Any]]:
        context = self.rag_system.query_knowledge_base(query)
        if not context or context.strip() == "":
            print("⚠️ WARNING: No documents found in knowledge base!")
            return self.create_fallback_test_cases(query, "")
        
        prompt = f"""You are a QA expert. Generate comprehensive test cases based on the user query and user uploaded documents.

User Query: {query}

Documentation Context:
{context}

Output Requirement:
Generate a MARKDOWN TABLE with the following columns. 
Do not include any text before or after the table.

Columns:
1. Test_ID (e.g., TC-001)
2. Feature
3. Test_Scenario
4. Test_Steps (Semicolon ';' separated list. E.g., "Step 1; Step 2; Step 3")
5. Expected_Result
6. Test_Type (Positive or Negative)
7. Grounded_In (Source document name)

CRITICAL REQUIREMENTS:
1. Base ALL test cases ONLY from the provided context.
2. Generate both Positive and Negative scenarios.
3. For 'Test_Steps', do not use newlines inside the cell. Use semicolons (;) to separate steps.
4. Ensure the 'Grounded_In' column references the specific file provided in context.
5. Generate at least 3 distinct test cases.

Output Format Example:
| Test_ID | Feature | Test_Scenario | Test_Steps | Expected_Result | Test_Type | Grounded_In |
| TC-001 | Login | Valid Login | Open app; Enter user; Click login | Dashboard loads | Positive | auth.md |
"""

        response = self.rag_system.llm.invoke(prompt).content
        test_cases = self.parse_markdown_response(response)
        if test_cases:
            print(f"✅ Successfully generated {len(test_cases)} test cases from documents")
            return test_cases
        else:
            print("⚠️ Parsing failed or no cases generated. Using fallback.")
            return self.create_fallback_test_cases(query, context)

    def parse_markdown_response(self, response: str) -> List[Dict[str, Any]]:
        #Parse table into dictionaries
        cases = []
        try:
            lines = response.strip().split('\n')
            header_index = -1
            for i, line in enumerate(lines):
                if set(line.strip()) <= {'|', '-', ' ', ':'}:
                    header_index = i
                    break
            if header_index == -1: 
                return []
            for line in lines[header_index + 1:]:
                if '|' not in line:
                    continue
                cells = [cell.strip() for cell in line.strip('|').split('|')]  
                if len(cells) < 7: 
                    continue
                raw_steps = cells[3]
                steps_list = [step.strip() for step in raw_steps.split(';') if step.strip()]
                
                test_case = {
                    "test_id": cells[0],
                    "feature": cells[1],
                    "test_scenario": cells[2],
                    "test_steps": steps_list, # Converted to list for UI
                    "expected_result": cells[4],
                    "test_type": cells[5],
                    "grounded_in": cells[6]
                }
                cases.append(test_case)
        except Exception as e:
            print(f"❌ Markdown parsing error: {str(e)}")
        return cases

    def create_fallback_test_cases(self, query: str, context: str) -> List[Dict[str, Any]]:
        return [
            {
                "test_id": "TC-001",
                "feature": "Manual Verification Needed",
                "test_scenario": f"Could not parse generated cases for: {query}",
                "test_steps": ["Check logs", "Verify LLM output format"],
                "expected_result": "Test cases generated",
                "test_type": "negative",
                "grounded_in": "System"
            }
        ]