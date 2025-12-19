from fortscript import FortScript

def main():
    app = FortScript(config_path="./config.yaml")
    app.run()

if __name__ == "__main__":
    main()