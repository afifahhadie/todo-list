import json
import os
from datetime import datetime

class TodoList:
    def __init__(self, filename="todos.json"):
        self.filename = filename
        self.todos = self.load_todos()
    
    def load_todos(self):
        """Load to-do data from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_todos(self):
        """Save to-do data to JSON file"""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.todos, file, indent=2, ensure_ascii=False)
    
    def add_todo(self, task, priority="medium"):
        """Add a new task"""
        todo = {
            "id": len(self.todos) + 1,
            "task": task,
            "completed": False,
            "priority": priority.lower(),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.todos.append(todo)
        self.save_todos()
        print(f"✅ Task '{task}' has been added successfully!")
    
    def view_todos(self, filter_completed=None):
        """Display all tasks"""
        if not self.todos:
            print("📝 No tasks in the list.")
            return
        
        # Filter by completed status
        filtered_todos = self.todos
        if filter_completed is not None:
            filtered_todos = [todo for todo in self.todos if todo["completed"] == filter_completed]
        
        if not filtered_todos:
            status = "completed" if filter_completed else "pending"
            print(f"📝 No {status} tasks.")
            return
        
        print("\n" + "="*60)
        print("                    TASK LIST")
        print("="*60)
        
        # Sort by priority
        priority_order = {"high": 1, "medium": 2, "low": 3}
        sorted_todos = sorted(filtered_todos, key=lambda x: priority_order.get(x["priority"], 2))
        
        for todo in sorted_todos:
            status = "✅" if todo["completed"] else "❌"
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(todo["priority"], "⚪")
            
            print(f"{status} [{todo['id']:2d}] {priority_icon} {todo['task']}")
            print(f"     Created: {todo['created_at']} | Priority: {todo['priority'].upper()}")
            print("-" * 60)
    
    def mark_completed(self, task_id):
        """Mark task as completed"""
        for todo in self.todos:
            if todo["id"] == task_id:
                todo["completed"] = True
                todo["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_todos()
                print(f"✅ Task '{todo['task']}' has been marked as completed!")
                return
        print(f"❌ Task with ID {task_id} not found.")
    
    def delete_todo(self, task_id):
        """Delete a task"""
        for i, todo in enumerate(self.todos):
            if todo["id"] == task_id:
                deleted_task = self.todos.pop(i)
                # Reorder IDs
                for j, remaining_todo in enumerate(self.todos):
                    remaining_todo["id"] = j + 1
                self.save_todos()
                print(f"🗑️ Task '{deleted_task['task']}' has been deleted successfully!")
                return
        print(f"❌ Task with ID {task_id} not found.")
    
    def edit_todo(self, task_id, new_task=None, new_priority=None):
        """Edit a task"""
        for todo in self.todos:
            if todo["id"] == task_id:
                if new_task:
                    old_task = todo["task"]
                    todo["task"] = new_task
                    print(f"✏️ Task successfully changed from '{old_task}' to '{new_task}'")
                
                if new_priority and new_priority.lower() in ["high", "medium", "low"]:
                    todo["priority"] = new_priority.lower()
                    print(f"🎯 Priority successfully changed to {new_priority.upper()}")
                
                todo["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_todos()
                return
        print(f"❌ Task with ID {task_id} not found.")
    
    def search_todos(self, keyword):
        """Search tasks by keyword"""
        found_todos = [todo for todo in self.todos if keyword.lower() in todo["task"].lower()]
        
        if not found_todos:
            print(f"🔍 No tasks found containing '{keyword}'.")
            return
        
        print(f"\n🔍 Search results for '{keyword}':")
        print("="*60)
        for todo in found_todos:
            status = "✅" if todo["completed"] else "❌"
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(todo["priority"], "⚪")
            print(f"{status} [{todo['id']:2d}] {priority_icon} {todo['task']}")
        print("="*60)

def show_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("           📝 TO-DO LIST SYSTEM 📝")
    print("="*50)
    print("1. ➕ Add task")
    print("2. 📋 View all tasks")
    print("3. ✅ Mark task as completed")
    print("4. 🗑️  Delete task") 
    print("5. ✏️  Edit task")
    print("6. 🔍 Search tasks")
    print("7. 📊 View completed tasks")
    print("8. 📋 View pending tasks")
    print("9. ❌ Exit")
    print("="*50)

def get_priority():
    """Get priority input from user"""
    while True:
        priority = input("Enter priority (high/medium/low) [default: medium]: ").strip().lower()
        if not priority:
            return "medium"
        if priority in ["high", "medium", "low"]:
            return priority
        print("❌ Priority must be 'high', 'medium', or 'low'")

def main():
    """Main application function"""
    todo_list = TodoList()
    
    print("🎉 Welcome to the To-Do List System!")
    
    while True:
        show_menu()
        
        try:
            choice = input("Choose menu (1-9): ").strip()
            
            if choice == "1":
                task = input("Enter new task: ").strip()
                if task:
                    priority = get_priority()
                    todo_list.add_todo(task, priority)
                else:
                    print("❌ Task cannot be empty!")
            
            elif choice == "2":
                todo_list.view_todos()
            
            elif choice == "3":
                todo_list.view_todos(filter_completed=False)
                if any(not todo["completed"] for todo in todo_list.todos):
                    try:
                        task_id = int(input("Enter task ID to mark as completed: "))
                        todo_list.mark_completed(task_id)
                    except ValueError:
                        print("❌ ID must be a number!")
            
            elif choice == "4":
                todo_list.view_todos()
                if todo_list.todos:
                    try:
                        task_id = int(input("Enter task ID to delete: "))
                        confirm = input(f"Are you sure you want to delete task with ID {task_id}? (y/n): ").lower()
                        if confirm == 'y':
                            todo_list.delete_todo(task_id)
                    except ValueError:
                        print("❌ ID must be a number!")
            
            elif choice == "5":
                todo_list.view_todos()
                if todo_list.todos:
                    try:
                        task_id = int(input("Enter task ID to edit: "))
                        print("Leave empty if you don't want to change:")
                        new_task = input("New task: ").strip()
                        new_priority = input("New priority (high/medium/low): ").strip()
                        
                        if new_task or new_priority:
                            todo_list.edit_todo(task_id, new_task if new_task else None, new_priority if new_priority else None)
                        else:
                            print("ℹ️ No changes made.")
                    except ValueError:
                        print("❌ ID must be a number!")
            
            elif choice == "6":
                keyword = input("Enter keyword to search: ").strip()
                if keyword:
                    todo_list.search_todos(keyword)
                else:
                    print("❌ Keyword cannot be empty!")
            
            elif choice == "7":
                print("\n📊 COMPLETED TASKS:")
                todo_list.view_todos(filter_completed=True)
            
            elif choice == "8":
                print("\n📋 PENDING TASKS:")
                todo_list.view_todos(filter_completed=False)
            
            elif choice == "9":
                print("👋 Thank you for using the To-Do List System!")
                print("💾 Your data has been saved automatically.")
                break
            
            else:
                print("❌ Invalid choice! Please choose 1-9.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Program terminated by user.")
            print("💾 Your data has been saved automatically.")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()