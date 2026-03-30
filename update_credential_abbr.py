#!/usr/bin/env python3
"""
Update SQL INSERT statements to add unique_credential_abbr column.
"""

import os
import re
from pathlib import Path


class CredentialUpdater:
    """Updates SQL files to add unique_credential_abbr column."""
    
    # Define duplicates with their IDs and suffixes
    DUPLICATES = {
        'AP': {20042: '_1', 50035: '_2'},
        'BT': {60033: '_1', 50067: '_2'},
        'CNN': {1174: '_1', 1177: '_2'},
        'CRN': {1145: '_1', 1214: '_2'},
        'MT': {60029: '_1', 50087: '_2'},
        'RN-BC': {
            1042: '_1', 1043: '_2', 1044: '_3', 1045: '_4',
            1047: '_5', 1049: '_6', 1050: '_7', 1051: '_8',
            1052: '_9', 1054: '_10', 1055: '_11', 1217: '_12'
        }
    }
    
    @staticmethod
    def process_sql_file(*, file_path: str) -> None:
        """
        Process a single SQL file to add unique_credential_abbr.
        
        Args:
            file_path: Path to the SQL file to process
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip files that don't have INSERT INTO dctnry.clinical_credential
            if 'INSERT INTO dctnry.clinical_credential' not in content:
                print(f"Skipping {file_path} - no credential inserts found")
                return
            
            # Update INSERT INTO column list to include unique_credential_abbr
            content = CredentialUpdater._update_insert_columns(content=content)
            
            # Update VALUES rows to include unique_credential_abbr
            content = CredentialUpdater._update_values_rows(content=content)
            
            # Write updated content back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Updated {file_path}")
            
        except Exception as e:
            raise Exception(f"CredentialUpdater.process_sql_file Error: Failed to process {file_path} - {str(e)}")
    
    @staticmethod
    def _update_insert_columns(*, content: str) -> str:
        """
        Update INSERT INTO column list to add unique_credential_abbr after credential_abbr.
        
        Args:
            content: SQL file content
            
        Returns:
            Updated content
        """
        # Pattern to find INSERT INTO with column list
        pattern = r'(INSERT INTO dctnry\.clinical_credential\s*\(\s*id,\s*credential_abbr,)'
        replacement = r'\1 unique_credential_abbr,'
        
        return re.sub(pattern, replacement, content)
    
    @staticmethod
    def _update_values_rows(*, content: str) -> str:
        """
        Update VALUES rows to add unique_credential_abbr value after credential_abbr.
        
        Args:
            content: SQL file content
            
        Returns:
            Updated content
        """
        lines = content.split('\n')
        updated_lines = []
        
        for line in lines:
            # Look for VALUES lines with format: (id, 'abbr', 'name', ...)
            match = re.match(r'^\s*\((\d+),\s*\'([^\']+)\',\s*\'', line)
            if match:
                id_val = int(match.group(1))
                abbr = match.group(2)
                
                # Determine unique_credential_abbr
                unique_abbr = CredentialUpdater._get_unique_abbr(id_val=id_val, abbr=abbr)
                
                # Insert unique_credential_abbr after credential_abbr
                # Pattern: (id, 'abbr', becomes (id, 'abbr', 'unique_abbr',
                line = re.sub(
                    r'(\(\d+,\s*\'[^\']+\',)\s*',
                    f"\\1 '{unique_abbr}', ",
                    line,
                    count=1
                )
            
            updated_lines.append(line)
        
        return '\n'.join(updated_lines)
    
    @staticmethod
    def _get_unique_abbr(*, id_val: int, abbr: str) -> str:
        """
        Get unique abbreviation for a credential.
        
        Args:
            id_val: Credential ID
            abbr: Original abbreviation
            
        Returns:
            Unique abbreviation with suffix if duplicate
        """
        # Check if this abbr is in duplicates
        if abbr in CredentialUpdater.DUPLICATES:
            id_map = CredentialUpdater.DUPLICATES[abbr]
            if id_val in id_map:
                return abbr + id_map[id_val]
        
        # Not a duplicate, return original
        return abbr
    
    @staticmethod
    def process_all_sql_files(*, sql_directory: str = "./sql/") -> None:
        """
        Process all SQL files in the directory.
        
        Args:
            sql_directory: Directory containing SQL files
        """
        try:
            sql_files = [
                'insert_credential_physicians.sql',
                'insert_credential_doctor_not_physician.sql',
                'insert_credential_nurses_batch1.sql',
                'insert_credential_nurses_batch2.sql',
                'insert_credential_midlevels.sql',
                'insert_credential_physical_therapists.sql',
                'insert_credential_psychosocial_therapists.sql',
                'insert_credential_other.sql',
                'insert_credential_animal_clinicians.sql',
                'insert_credential_not_clinicians.sql',
            ]
            
            for sql_file in sql_files:
                file_path = os.path.join(sql_directory, sql_file)
                if os.path.exists(file_path):
                    CredentialUpdater.process_sql_file(file_path=file_path)
                else:
                    print(f"Warning: File not found - {file_path}")
            
            print(f"\nSuccessfully processed {len(sql_files)} SQL files")
            
        except Exception as e:
            raise Exception(f"CredentialUpdater.process_all_sql_files Error: {str(e)}")


def main():
    """Main function to execute SQL file updates."""
    try:
        CredentialUpdater.process_all_sql_files()
        print("\n✓ All SQL files updated successfully!")
        print("Next step: Run merge_sql.py to generate merged SQL file")
    except Exception as e:
        print(f"update_credential_abbr.py Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
