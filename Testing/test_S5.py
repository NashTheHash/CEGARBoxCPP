#!/usr/bin/env python3
from pathlib import Path
import os
import re
import shutil
import subprocess
import sys
import tempfile


#CONVERTS MODAL FORMULAE TO CEGAR FRIENDLY FORMAT
def Convert_Formula(formula):
   
    conversions = {
        '□': '[1]',
        '◇': '<1>', 
        '¬': '~',
        '∨': '|',
        '∧': '&',
        '→': '=>',
        '↔': '<=>'
    }

    formula = formula.strip()
    
    for logical_symbol, plaintext_version in conversions.items():
        formula = formula.replace(logical_symbol, plaintext_version)
    
    #THE SUBSCRIPT SHOULD BE IN THE OPERATOR 
    formula = formula.replace('[1]1', '[1]')
    formula = formula.replace('<1>1', '<1>')
    
    #REMOVE SPACES
    formula = re.sub(r'\s+', '', formula)
    
    return formula


class KaleidoscopeTester:
    def __init__(self):
        self.program = "./kaleidoscope"
        self.test_directory = "Testing/Tests"
        self.expected_results = {}
        self.temp_directory = tempfile.mkdtemp(prefix="kaleidoscope_tests_")
      
        
    #CLEANS UP TEMPORARY FILES
    def __del__(self):
        if os.path.exists(self.temp_directory):
            shutil.rmtree(self.temp_directory)
    

    #EXTRACTS THE EXPECTED RESULT FROM THE FILENAME. TRANSLATION INVARIANT.
    def Get_Expected_Result(self, filename):
        
        filename = filename.lower().replace('.txt', '')
        
        if re.search(r'unsat(_|\b)', filename):
            return 'Unsatisfiable'

        if re.search(r'sat(_|\b)', filename):
            return 'Satisfiable'
        else:
            raise ValueError("Cannot identify expected result")
    

    #SAVE CONVERTED FORMULAE TO TEMPORARY FILE
    def Convert_And_Save(self, path):
        
        try:
            with open(path, 'r') as f:
                formula = f.read()
            
            new_formula = Convert_Formula(formula)
            
            temp_file = f"converted_{path.name}"
            temp_path = os.path.join(self.temp_directory, temp_file)
            
            with open(temp_path, 'w') as f:
                f.write(new_formula)
            
            return temp_path, formula, new_formula
            
        except Exception as e:
            print(f"Error converting file {path}: {e}")
            return str(path), "Error reading", "Error converting"


    #RUN SINGLE TEST
    def Run_Test(self, path):
        
        filename = path.name
        expected = self.Get_Expected_Result(filename)
        temp_file, formula, new_formula = self.Convert_And_Save(path)
        
        #THE COMMAND THAT GOES INTO THE TERMINAL
        cmd = [self.program, "-f", temp_file, "-t", "-5"]
        
        #print(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout.split('\n')[0].strip() if result.stdout else ""
         
            
            return {
                'filename': filename,
                'filepath': str(path),
                'exit_code': result.returncode,
                'output': output,
                'expected': expected,
                'success': result.returncode == 0,
                'matches_expected': expected is not None and output == expected,
                'error': result.stderr.strip() if result.stderr else None,
                'timed_out': False,
                'original_formula': formula,
                'converted_formula': new_formula,
            }
            
        except subprocess.TimeoutExpired:
            return {
                'filename': filename,
                'filepath': str(path),
                'exit_code': -1,
                'output': '',
                'expected': expected,
                'success': False,
                'matches_expected': False,
                'error': 'Timeout after 30 seconds',
                'timed_out': True,
                'original_formula': formula,
                'converted_formula': new_formula,
            }
        
        except Exception as e:
            return {
                'filename': filename,
                'filepath': str(path),
                'exit_code': -1,
                'output': '',
                'expected': expected,
                'success': False,
                'matches_expected': False,
                'error': f'Unexpected error: {e}',
                'timed_out': False,
                'original_formula': formula,
                'converted_formula': new_formula,
            }
    

    def Print_Result(self, result):
       
        filename = result['filename']
        
        if result['timed_out']:
            status = "TIMEOUT"
            color = '\033[93m'

        elif not result['success']:
            status = "FAILED"
            color = '\033[91m'

        elif result['matches_expected']:
            status = "PASSED"
            color = '\033[92m'
        else:
            status = "FAILED (wrong output)"
            color = '\033[91m'
        
        print(f"{color}{status:<20}\033[0m {filename}")
    
        if result['error']:
            print(f"  Error: {result['error']}")

        elif not result['matches_expected']:
            print(f"  Expected: '{result['expected']}'")
    

    def Summarise_Results(self, results):

        total = len(results)
        passed = sum(
            1 for result in results if result['success'] and result['matches_expected']
        )
        unsucessful = sum(1 for result in results if not result['success'])
        failed = total - passed - unsucessful
        
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Total tests:    {total}")
        print(f"Passed:         {passed}")
        print(f"Failed:         {failed}")
        print(f"Unsuccessful:   {unsucessful}")

        failed_tests = [result for result in results if not result['success'] or not result['matches_expected']]

        if failed_tests:
            print("\nFAILED TESTS:")
            for result in failed_tests:
                if result['timed_out']:
                    status = "TIMEOUT"
                elif not result['success']:
                    status = "EXECUTION FAILED"
                else:
                    status = "WRONG OUTPUT"
                print(f"  {result['filename']} ({status})")
        
        return 1 if failed_tests else 0


    def Run_All_Tests(self):
       
        if not os.path.exists(self.program):
            print(f"Error: Program {self.program} not found")
            return 1
            
        if not os.path.isdir(self.test_directory):
            print(f"Error: Test directory {self.test_directory} not found")
            return 1
        
        test_files = list(Path(self.test_directory).glob("*.txt"))

        if not test_files:
            print(f"No text files found in {self.test_directory}")
            return 0
        
        print(f"Running {len(test_files) + 1} test(s) from '{self.test_directory}' directory")
        print(f"Temporary files in: {self.temp_directory}")
        print("=" * 60)
        
        results = []

        for test_file in sorted(test_files):
            result = self.Run_Test(test_file)
            results.append(result)
            self.Print_Result(result)
        
        return self.Summarise_Results(results)
    

tester = KaleidoscopeTester()
sys.exit(tester.Run_All_Tests())