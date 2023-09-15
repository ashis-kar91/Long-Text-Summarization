from fastapi import FastAPI, UploadFile
import os
import summarize

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    try:
        contents = file.file.read()
        input_path = 'input_files'
        if not os.path.exists(input_path):
            os.makedirs(input_path)
        file_path = f'{input_path}/{file.filename}'
        with open(file_path, "wb") as f:
            f.write(contents)
        return summarize.main(file_path)
    except Exception as exp_obj:
        return {"message": f"Error generating summary. {exp_obj}"}
    finally:
        file.file.close()