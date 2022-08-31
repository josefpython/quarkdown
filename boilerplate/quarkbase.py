from markdown import markdown

class QuarkBase:
    def __init__(self, repository_url: str) -> None:
        self.repository_url = repository_url

    def check_and_update(self):
        """
        TODO Check repository for not yet rendered articles, fetch them,
        run them into self.render_article() & render new landing using self.render_landing()
        """
        pass
        

    def render_article(self, quark_string: str, id: int) -> dict:
        """
        Parses a .qd file (provided as a string) and creates a file
        in the templates folder accordingly.
        """
        head_allowed_settings = ["DOCUMENT_TITLE", "TITLE", "AUTHOR", "DATE", "SYNTAX"]
        #extract head & body
        try:
            raw_head = quark_string.split("<$HEAD$>")[1].split("<$ENDHEAD$>")[0]
            raw_body = quark_string.split("<$BODY$>")[1].split("<$ENDBODY$>")[0]
            try:     
                settings = {}
                head_lines = raw_head.split("\n")

                for setting in head_lines:

                    if setting == "":
                        continue

                    _key, _value = setting.split("::")

                    if not (_key in head_allowed_settings):
                        raise ValueError

                    if _key == "SYNTAX" and not (_value in ["md", "html"]):
                        raise ValueError

                    settings[_key] = _value             
                try:
                    with open("templates/article_"+str(id)+".html", "w") as f:
                        
                        if settings["SYNTAX"] == "html":    
                            f.write(raw_body)            
                        elif settings["SYNTAX"] == "md":
                            try:
                                cmd = markdown(raw_body)
                                cmd = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>'+settings["DOCUMENT_TITLE"]+'</title></head><body>'+cmd+'</body></html>'
                                f.write(cmd)
                            except Exception:
                                return {
                                    "sucess": False,
                                    "status": "Markdown conversion failed."
                                }
                except Exception:
                    return {
                        "success": False,
                        "status": "Critical error: couldnt create article?"
                            }
                return {
                    "sucess": True,
                    "status": "Created articles."
                }
            except (ValueError, KeyError):
                return {
                    "success": False,
                    "status": "Critical error: head of quarkdown file invalid!"
                    } 
        except (ValueError, KeyError):
            return {
                "success": False,
                "status": "Critical error: head or body tag not found in quarkdown file!"
                }

    def render_landing(self, path) -> int:
        return 1


if __name__ == "__main__":
    with open("example_landing.qd", "r") as f:
        base = QuarkBase()
        print(base.render_article(f.read(),1))