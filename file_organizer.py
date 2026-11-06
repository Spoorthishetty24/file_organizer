import os
import shutil
from pathlib import Path

def undo_organization(directory_path):
    """
    Moves all files from organized folders back to the main directory.
    
    Args:
        directory_path (str): Path to the directory to restore
    """
    directory = Path(directory_path).resolve()
    
    # Check if the directory exists
    if not directory.exists():
        print(f"Error: The directory '{directory}' does not exist.")
        return
    
    print(f"\nRestoring files from organized folders in: {directory}\n")
    
    # List of category folders to check
    category_folders = ['Images', 'Documents', 'Videos', 'Audio', 'Archives', 
                       'Code', 'Executables', 'Others']
    
    files_moved = 0
    
    # Go through each category folder
    for category in category_folders:
        category_path = directory / category
        
        # Skip if folder doesn't exist
        if not category_path.exists():
            continue
        
        print(f"Checking {category} folder...")
        
        # Move all files from this category back to main directory
        for item in category_path.iterdir():
            if item.is_file():
                destination = directory / item.name
                
                # Handle duplicate filenames
                counter = 1
                original_destination = destination
                while destination.exists():
                    stem = original_destination.stem
                    suffix = original_destination.suffix
                    destination = directory / f"{stem}_restored_{counter}{suffix}"
                    counter += 1
                
                try:
                    shutil.move(str(item), str(destination))
                    print(f"✓ Restored: {item.name}")
                    files_moved += 1
                except Exception as e:
                    print(f"✗ Error restoring {item.name}: {e}")
        
        # Remove empty category folder
        try:
            if not any(category_path.iterdir()):
                category_path.rmdir()
                print(f"  Removed empty folder: {category}")
        except Exception as e:
            print(f"  Could not remove {category} folder: {e}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Restore complete! {files_moved} files moved back.")
    print(f"{'='*50}\n")


def organize_files(directory_path, dry_run=False):
    """
    Organizes files in a directory into folders based on their file type.
    
    Args:
        directory_path (str): Path to the directory to organize
        dry_run (bool): If True, only shows what would happen without moving files
    """
    
    # Define file type categories and their extensions
    file_categories = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.webp'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.ppt', '.pptx', '.csv'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
        'Code': ['.py', '.java', '.cpp', '.c', '.js', '.html', '.css', '.php', '.sql'],
        'Executables': ['.exe', '.msi', '.app', '.deb', '.rpm']
    }
    
    # Convert the path to an absolute path
    directory = Path(directory_path).resolve()
    
    # Check if the directory exists
    if not directory.exists():
        print(f"Error: The directory '{directory}' does not exist.")
        return
    
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory.")
        return
    
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Organizing files in: {directory}\n")
    
    if dry_run:
        print("🔍 DRY RUN MODE - No files will be moved\n")
    
    # Counter for tracking organized files
    files_moved = 0
    
    # Iterate through all items in the directory
    for item in directory.iterdir():
        # Skip if item is a directory
        if item.is_dir():
            continue
        
        # Get the file extension (lowercase for comparison)
        file_extension = item.suffix.lower()
        
        # Skip files without extensions
        if not file_extension:
            continue
        
        # Find the appropriate category for this file
        category_found = False
        for category, extensions in file_categories.items():
            if file_extension in extensions:
                # Create the category folder if it doesn't exist
                category_path = directory / category
                category_path.mkdir(exist_ok=True)
                
                # Define the destination path
                destination = category_path / item.name
                
                # Handle duplicate filenames
                counter = 1
                original_destination = destination
                while destination.exists():
                    # Add a number to the filename if it already exists
                    stem = original_destination.stem
                    suffix = original_destination.suffix
                    destination = category_path / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                # Move the file
                try:
                    if dry_run:
                        # Just preview, don't actually move
                        print(f"[PREVIEW] Would move: {item.name} → {category}/")
                    else:
                        shutil.move(str(item), str(destination))
                        print(f"✓ Moved: {item.name} → {category}/")
                    files_moved += 1
                    category_found = True
                    break
                except Exception as e:
                    print(f"✗ Error moving {item.name}: {e}")
        
        # If no category found, move to "Others" folder
        if not category_found:
            others_path = directory / "Others"
            others_path.mkdir(exist_ok=True)
            
            destination = others_path / item.name
            
            # Handle duplicates
            counter = 1
            original_destination = destination
            while destination.exists():
                stem = original_destination.stem
                suffix = original_destination.suffix
                destination = others_path / f"{stem}_{counter}{suffix}"
                counter += 1
            
            try:
                if dry_run:
                    # Just preview, don't actually move
                    print(f"[PREVIEW] Would move: {item.name} → Others/")
                else:
                    shutil.move(str(item), str(destination))
                    print(f"✓ Moved: {item.name} → Others/")
                files_moved += 1
            except Exception as e:
                print(f"✗ Error moving {item.name}: {e}")
    
    # Summary
    print(f"\n{'='*50}")
    if dry_run:
        print(f"Preview complete! {files_moved} files would be moved.")
        print("Run again without dry run mode to actually organize files.")
    else:
        print(f"Organization complete! {files_moved} files moved.")
    print(f"{'='*50}\n")


def main():
    """
    Main function to run the file organizer.
    """
    print("=" * 50)
    print("FILE ORGANIZER SCRIPT")
    print("=" * 50)
    
    # Get directory path from user
    directory_path = input("\nEnter the full path of the directory to organize: ").strip()
    
    # Remove quotes if user copied path with quotes
    directory_path = directory_path.strip('"').strip("'")
    
    # Ask if user wants to preview first
    print("\nChoose an option:")
    print("1. Preview only (see what would happen)")
    print("2. Organize files (actually move them)")
    print("3. UNDO - Move all files back to main folder")
    choice = input("\nEnter your choice (1, 2, or 3): ").strip()
    
    if choice == '1':
        # Run in dry run mode (preview only)
        organize_files(directory_path, dry_run=True)
    elif choice == '2':
        # Confirm before proceeding
        print(f"\nYou are about to organize files in: {directory_path}")
        confirmation = input("Do you want to proceed? (yes/no): ").strip().lower()
        
        if confirmation in ['yes', 'y']:
            organize_files(directory_path, dry_run=False)
        else:
            print("\nOperation cancelled.")
    elif choice == '3':
        # Undo organization
        print(f"\nYou are about to move all files back to: {directory_path}")
        confirmation = input("Do you want to proceed? (yes/no): ").strip().lower()
        
        if confirmation in ['yes', 'y']:
            undo_organization(directory_path)
        else:
            print("\nOperation cancelled.")
    else:
        print("\nInvalid choice. Operation cancelled.")


# Run the script
if __name__ == "__main__":
    main()