import re

# Define the version pattern for CMakeLists.txt
cmake_version_pattern = re.compile(
    r"(set\(VERSION_MAJOR\s+)(\d+)(\))\s*"
    r"(set\(VERSION_MINOR\s+)(\d+)(\))\s*"
    r"(set\(VERSION_PATCH\s+)(\d+)(\))"
)

# Define the version pattern for README.md (e.g., "Version: 1.0.0")
readme_version_pattern = re.compile(r"(Version:\s+)(\d+)\.(\d+)\.(\d+)")

def increment_version_cmake(content):
    match = cmake_version_pattern.search(content)
    if match:
        major = int(match.group(2))
        minor = int(match.group(5))
        patch = int(match.group(8))
        
        # Simple example: increment patch version
        patch += 1
        
        new_content = cmake_version_pattern.sub(
            rf"\g<1>{major}\g<3>\n\g<4>{minor}\g<6>\n\g<7>{patch}\g<9>",
            content
        )
        return new_content, major, minor, patch
    else:
        raise ValueError("Version pattern not found in CMakeLists.txt")

def update_readme_version(content, major, minor, patch):
    new_content = readme_version_pattern.sub(
        rf"\g<1>{major}.{minor}.{patch}",
        content
    )
    return new_content

def main():
    # Update CMakeLists.txt
    cmake_file = "NetworkManager/CMakeLists.txt"
    try:
        with open(cmake_file, "r") as file:
            cmake_content = file.read()
        
        new_cmake_content, major, minor, patch = increment_version_cmake(cmake_content)
        
        with open(cmake_file, "w") as file:
            file.write(new_cmake_content)
        
        print(f"Version updated in {cmake_file} to {major}.{minor}.{patch}")
        
        # Update README.md in a different location
        readme_file = "docs/api/NetworkManagerPlugin.md"
        with open(readme_file, "r") as file:
            readme_content = file.read()
        
        new_readme_content = update_readme_version(readme_content, major, minor, patch)
        
        with open(readme_file, "w") as file:
            file.write(new_readme_content)
        
        print(f"Version updated in {readme_file} to {major}.{minor}.{patch}")
    
    except FileNotFoundError:
        print(f"Error: File '{cmake_file}' or '{readme_file}' not found.")
    except ValueError as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
