from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.models import PromptRequest, GenerationResponse
from app.inference import inference_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        inference_engine.load_model()
    except Exception as e:
        print(f"Ошибка при загрузке модели: {e}")
    yield
    print("Сервер остановлен.")

app = FastAPI(title="GenAI API", lifespan=lifespan)

@app.get("/")
async def root():
    """Информация о сервисе"""
    return {
        "service": "GenAI API",
        "version": "1.0.0",
        "description": "Fine-tuned LLM inference API"
    }

@app.get("/health")
async def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "ok"}

@app.post("/generate", response_model=GenerationResponse)
async def generate_text(request: PromptRequest):
    """Генерация текста по промпту"""
    try:
        # Получаем сгенерированный текст и количество токенов
        response_text, tokens = inference_engine.generate(request.prompt, request.max_tokens)
        
        return GenerationResponse(
            prompt=request.prompt,
            response=response_text,
            model=inference_engine.model_path,
            tokens_used=tokens
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")