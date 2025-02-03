def srt_to_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    processed_lines = []
    i = 1
    for line in lines:
        if i == 3:
            processed_lines.append(line)
            i += 1
        elif i == 4:
            i = 1
        else:
            i += 1
            
        
    with open("captions.txt", 'w', encoding='utf-8') as file:
        file.writelines(processed_lines)
    print(f"File '{file_path}' has been updated.")

# Example usage:
file_path = 'captions.srt'  # Replace with your actual file path
srt_to_txt(file_path)
