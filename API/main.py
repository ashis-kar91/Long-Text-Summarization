from fastapi import FastAPI, UploadFile
import summarize

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    try:
        contents = file.file.read()
        file_path = f'input_files/{file.filename}'
        with open(file_path, "wb") as f:
            f.write(contents)
        return summarize.main(file_path)
    except Exception as exp_obj:
        return {"message": f"Error generating summary. {exp_obj}"}
    finally:
        file.file.close()