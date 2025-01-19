from app import create_app

app = create_app()




if __name__ == "__main__":
    print(f"Template Folder: {app.template_folder}")
    #print(app.c)
    app.run(debug=True)
