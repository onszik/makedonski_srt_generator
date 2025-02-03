def remove_frequencies_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Process each line to keep only the word and new lines
    processed_lines = []
    for line in lines:
        # Split the line by space and keep only the word (first part)
        word = line.split()[0]
        processed_lines.append(word + '\n')  # Add back the newline
        
    # Write the processed content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(processed_lines)
    print(f"File '{file_path}' has been updated.")

# Example usage:
file_path = 'mk_full.txt'  # Replace with your actual file path
remove_frequencies_from_file(file_path)
