"""
Database Manager - Universal database connection and management tool
Supports SQLite, PostgreSQL, MySQL, and MongoDB
"""

import os
import json
import sqlite3
from typing import Dict, Optional, List, Any, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime

console = Console()


class DatabaseManager:
    """Universal database manager for multiple database types"""
    
    def __init__(self):
        self.connections = {}
        self.active_connection = None
        self.connection_type = None
        self._load_connections()
    
    def _load_connections(self):
        """Load saved database connections"""
        try:
            conn_path = os.path.join(os.path.expanduser("~"), ".nexus", "db_connections.json")
            if os.path.exists(conn_path):
                with open(conn_path, 'r') as f:
                    saved = json.load(f)
                    # Only load connection configs, not actual connections
                    self.connections = {k: v for k, v in saved.items()}
        except Exception as e:
            console.print(f"[yellow]Warning: Could not load connections: {e}[/yellow]")
    
    def _save_connections(self):
        """Save connection configurations"""
        try:
            conn_path = os.path.join(os.path.expanduser("~"), ".nexus", "db_connections.json")
            os.makedirs(os.path.dirname(conn_path), exist_ok=True)
            with open(conn_path, 'w') as f:
                json.dump(self.connections, f, indent=2)
        except Exception as e:
            console.print(f"[red]Error saving connections: {e}[/red]")
    
    def connect(self, db_type: str, connection_string: str, name: str = "default") -> str:
        """Connect to a database"""
        try:
            db_type = db_type.lower()
            
            if db_type == "sqlite":
                return self._connect_sqlite(connection_string, name)
            elif db_type == "postgresql" or db_type == "postgres":
                return self._connect_postgresql(connection_string, name)
            elif db_type == "mysql":
                return self._connect_mysql(connection_string, name)
            elif db_type == "mongodb" or db_type == "mongo":
                return self._connect_mongodb(connection_string, name)
            else:
                return f"❌ Unsupported database type: {db_type}\n   Supported: sqlite, postgresql, mysql, mongodb"
        
        except Exception as e:
            return f"❌ Connection error: {str(e)}"
    
    def _connect_sqlite(self, path: str, name: str) -> str:
        """Connect to SQLite database"""
        try:
            conn = sqlite3.connect(path)
            self.connections[name] = {
                "type": "sqlite",
                "path": path,
                "connection": conn,
                "connected_at": datetime.now().isoformat()
            }
            self.active_connection = name
            self.connection_type = "sqlite"
            self._save_connections()
            
            return f"✅ Connected to SQLite database: {path}\n   Connection name: {name}"
        except Exception as e:
            return f"❌ SQLite connection failed: {str(e)}"
    
    def _connect_postgresql(self, connection_string: str, name: str) -> str:
        """Connect to PostgreSQL database"""
        try:
            import psycopg2
            conn = psycopg2.connect(connection_string)
            self.connections[name] = {
                "type": "postgresql",
                "connection_string": connection_string,
                "connection": conn,
                "connected_at": datetime.now().isoformat()
            }
            self.active_connection = name
            self.connection_type = "postgresql"
            return f"✅ Connected to PostgreSQL database\n   Connection name: {name}"
        except ImportError:
            return "❌ psycopg2 not installed. Run: pip install psycopg2-binary"
        except Exception as e:
            return f"❌ PostgreSQL connection failed: {str(e)}"
    
    def _connect_mysql(self, connection_string: str, name: str) -> str:
        """Connect to MySQL database"""
        try:
            import mysql.connector
            # Parse connection string or use as host
            conn = mysql.connector.connect(connection_string)
            self.connections[name] = {
                "type": "mysql",
                "connection_string": connection_string,
                "connection": conn,
                "connected_at": datetime.now().isoformat()
            }
            self.active_connection = name
            self.connection_type = "mysql"
            return f"✅ Connected to MySQL database\n   Connection name: {name}"
        except ImportError:
            return "❌ mysql-connector-python not installed. Run: pip install mysql-connector-python"
        except Exception as e:
            return f"❌ MySQL connection failed: {str(e)}"
    
    def _connect_mongodb(self, connection_string: str, name: str) -> str:
        """Connect to MongoDB database"""
        try:
            from pymongo import MongoClient
            client = MongoClient(connection_string)
            # Test connection
            client.server_info()
            self.connections[name] = {
                "type": "mongodb",
                "connection_string": connection_string,
                "connection": client,
                "connected_at": datetime.now().isoformat()
            }
            self.active_connection = name
            self.connection_type = "mongodb"
            return f"✅ Connected to MongoDB\n   Connection name: {name}"
        except ImportError:
            return "❌ pymongo not installed. Run: pip install pymongo"
        except Exception as e:
            return f"❌ MongoDB connection failed: {str(e)}"
    
    def list_connections(self) -> str:
        """List all database connections"""
        if not self.connections:
            return "📋 No database connections configured"
        
        table = Table(title="🗄️ Database Connections", show_header=True, header_style="bold cyan")
        table.add_column("Name", style="white")
        table.add_column("Type", style="yellow")
        table.add_column("Status", style="green")
        table.add_column("Connected At", style="dim")
        
        for name, conn_info in self.connections.items():
            status = "✅ Active" if name == self.active_connection else "⚪ Inactive"
            conn_time = conn_info.get('connected_at', 'Unknown')
            table.add_row(
                name,
                conn_info['type'],
                status,
                conn_time
            )
        
        console.print(table)
        return ""
    
    def query(self, sql: str) -> str:
        """Execute SQL query"""
        if not self.active_connection:
            return "❌ No active database connection. Use /db connect first"
        
        try:
            conn_info = self.connections[self.active_connection]
            conn = conn_info['connection']
            db_type = conn_info['type']
            
            if db_type == "mongodb":
                return "❌ Use MongoDB-specific commands for NoSQL queries"
            
            cursor = conn.cursor()
            cursor.execute(sql)
            
            # Check if it's a SELECT query
            if sql.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                if not rows:
                    return "📋 Query returned no results"
                
                # Create table for results
                table = Table(title=f"📊 Query Results ({len(rows)} rows)", 
                            show_header=True, header_style="bold cyan")
                
                for col in columns:
                    table.add_column(col, style="white")
                
                for row in rows[:100]:  # Limit to 100 rows
                    table.add_row(*[str(val) for val in row])
                
                console.print(table)
                
                if len(rows) > 100:
                    return f"\n⚠️ Showing first 100 of {len(rows)} rows"
                return ""
            else:
                # For INSERT, UPDATE, DELETE, etc.
                conn.commit()
                return f"✅ Query executed successfully\n   Rows affected: {cursor.rowcount}"
        
        except Exception as e:
            return f"❌ Query error: {str(e)}"
    
    def show_tables(self) -> str:
        """Show all tables in database"""
        if not self.active_connection:
            return "❌ No active database connection"
        
        try:
            conn_info = self.connections[self.active_connection]
            db_type = conn_info['type']
            
            if db_type == "sqlite":
                query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            elif db_type == "postgresql":
                query = "SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename"
            elif db_type == "mysql":
                query = "SHOW TABLES"
            else:
                return "❌ Table listing not supported for this database type"
            
            return self.query(query)
        
        except Exception as e:
            return f"❌ Error listing tables: {str(e)}"
    
    def describe_table(self, table_name: str) -> str:
        """Show table schema"""
        if not self.active_connection:
            return "❌ No active database connection"
        
        try:
            conn_info = self.connections[self.active_connection]
            db_type = conn_info['type']
            
            if db_type == "sqlite":
                query = f"PRAGMA table_info({table_name})"
            elif db_type == "postgresql":
                query = f"SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name='{table_name}'"
            elif db_type == "mysql":
                query = f"DESCRIBE {table_name}"
            else:
                return "❌ Schema description not supported for this database type"
            
            return self.query(query)
        
        except Exception as e:
            return f"❌ Error describing table: {str(e)}"
    
    def backup(self, output_path: str) -> str:
        """Backup database"""
        if not self.active_connection:
            return "❌ No active database connection"
        
        try:
            conn_info = self.connections[self.active_connection]
            db_type = conn_info['type']
            
            if db_type == "sqlite":
                import shutil
                source = conn_info['path']
                shutil.copy2(source, output_path)
                size = os.path.getsize(output_path)
                return f"✅ Database backup created\n   File: {output_path}\n   Size: {size:,} bytes"
            else:
                return "❌ Backup currently only supported for SQLite\n   Use native database tools for PostgreSQL/MySQL"
        
        except Exception as e:
            return f"❌ Backup error: {str(e)}"
    
    def stats(self) -> str:
        """Show database statistics"""
        if not self.active_connection:
            return "❌ No active database connection"
        
        try:
            conn_info = self.connections[self.active_connection]
            db_type = conn_info['type']
            
            stats = []
            stats.append(f"🗄️ Database Statistics")
            stats.append(f"Type: {db_type}")
            stats.append(f"Connection: {self.active_connection}")
            
            if db_type == "sqlite":
                path = conn_info['path']
                size = os.path.getsize(path) if os.path.exists(path) else 0
                stats.append(f"Size: {size:,} bytes ({size/1024/1024:.2f} MB)")
                
                # Count tables
                conn = conn_info['connection']
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
                table_count = cursor.fetchone()[0]
                stats.append(f"Tables: {table_count}")
            
            return "\n".join(stats)
        
        except Exception as e:
            return f"❌ Error getting stats: {str(e)}"
    
    def execute_script(self, script_path: str) -> str:
        """Execute SQL script from file"""
        if not self.active_connection:
            return "❌ No active database connection"
        
        try:
            if not os.path.exists(script_path):
                return f"❌ Script file not found: {script_path}"
            
            with open(script_path, 'r') as f:
                script = f.read()
            
            conn_info = self.connections[self.active_connection]
            conn = conn_info['connection']
            
            cursor = conn.cursor()
            cursor.executescript(script) if self.connection_type == "sqlite" else cursor.execute(script)
            conn.commit()
            
            return f"✅ Script executed successfully\n   File: {script_path}"
        
        except Exception as e:
            return f"❌ Script execution error: {str(e)}"
    
    def close(self, name: Optional[str] = None) -> str:
        """Close database connection"""
        try:
            target = name or self.active_connection
            if not target or target not in self.connections:
                return "❌ No connection to close"
            
            conn_info = self.connections[target]
            if 'connection' in conn_info and conn_info['connection']:
                conn_info['connection'].close()
            
            del self.connections[target]
            
            if target == self.active_connection:
                self.active_connection = None
                self.connection_type = None
            
            return f"✅ Connection '{target}' closed"
        
        except Exception as e:
            return f"❌ Error closing connection: {str(e)}"
