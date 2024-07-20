# SCHOOL MANAGEMENT SYSTEM...

# Importing
from typing import Final
from time import sleep
from sys import exit
import mysql.connector as msc
import src
from dotenv import load_dotenv,find_dotenv
from os import getenv
from getpass import getpass
from rich.console import Console
from rich import print as rprint
from rich.table import Table

load_dotenv(find_dotenv())
console = Console()

# Declaring ENV Variables 

MYSQL_HOST: Final = getenv('MYSQL_HOST')
MYSQL_PORT: Final = getenv('MYSQL_PORT')
MYSQL_USER: Final = getenv('MYSQL_USER')
MYSQL_PASSWORD: Final = getenv('MYSQL_PASSWORD')
MYSQL_DATABASE: str = getenv('MYSQL_DATABASE')

def main():

    rprint("Enter the password")
    inputPassword: str = getpass(':')

    src.Enter()

    with console.status("[bold green]Verifying Password..") as status:
        sleep(3)
        if inputPassword != MYSQL_PASSWORD:
            console.log("[bold red]ACCESS DENIED![/bold red]")
            exit()
        else:
            console.log("[green]Password Verified![/green]")

    with console.status("[bold green]Checking for MYSQL Connection..") as status:
        sleep(3)
        try:
            connection = msc.connect(host = MYSQL_HOST , port = MYSQL_PORT , user = MYSQL_USER , passwd = MYSQL_PASSWORD)
            cursor = connection.cursor()
            if connection.is_connected():
                console.log(f"[green]Connection Established ![/green]")
        except:
            console.log(f'[bold][red]Unable to Connect to MYSQL Server ')
            exit()

    
    with console.status("[bold green]Checking for Database..") as status:
        sleep(2)
        if MYSQL_DATABASE == '':
            console.log(f'[bold][red]Database Not Defined. ')
            database = False
        else:
            database = MYSQL_DATABASE
            console.log(f'[bold][green]Database Found. ')
   
    if not database:
        database  = src.create_database(cursor,console)
    connection = msc.connect(host = MYSQL_HOST , port = MYSQL_PORT , user = MYSQL_USER , passwd = MYSQL_PASSWORD , database = database)
    cursor = connection.cursor()
    src.create_table(cursor,console)

    while True:
        src.Enter()
        table = Table(title="Akkupy School")
        table.add_column("S. No.", style="cyan", no_wrap=True)
        table.add_column("Section", style="magenta")
        table.add_row("1","Students")
        table.add_row("2","Teachers")
        table.add_row("3","Classes")
        table.add_row("4","Exit")
        console.print(table)
        sectionValue = src.Choice("Enter a Choice(1,2,3,4)", [1, 2, 3, 4])

        match sectionValue:
            case 1:
                src.Student(cursor,connection,console)
            case 2:
                src.Teachers(cursor,connection,console)
            case 3:
                src.Class(cursor,connection,console)
            case 4:
                with console.status("[red bold]Quitting Program....[/red bold]") as status:
                    sleep(3)
                    connection.close()
                    console.log("[bold red] Bye.[/bold red]")
                    exit()



if __name__=="__main__":
    main()