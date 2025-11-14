from app.config.config import GROQ_API_KEY, MODEL_NAME
from app.components.llm import load_llm
from app.components.vector_store import load_vector_store
from app.components.prompt_template import prompt
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def create_qa_chain():
    try:
        logger.info("Loading vector store for context")
        db = load_vector_store()
        if db is None:
            raise CustomException("Vector store not present or empty")

        llm = load_llm(api_key=GROQ_API_KEY, model_name=MODEL_NAME)
        if llm is None:
            raise CustomException("LLM not loaded")

        prompt_template = prompt()
        logger.info("Successfully created custom QA retriever")
        
        def qa_run(query: str, history: list = None):
            try:
                # Retrieve relevant documents
                retriever = db.as_retriever(search_kwargs={"k": 1})
                docs = retriever.invoke(query)

                # Concatenate retrieved context
                context = "\n".join([doc.page_content for doc in docs])

                # Build conversation history string
                history_text = ""
                if history:
                    for msg in history:
                        role = "User" if msg["role"] == "user" else "Assistant"
                        history_text += f"{role}: {msg['content']}\n"

                # Format the prompt with both context and history
                prompt_input = prompt_template.format(
                    context=context,
                    question=query,
                    history=history_text
                )

                # Run the LLM
                response = llm.invoke(prompt_input)
                return response.content if hasattr(response, "content") else str(response)

            except Exception as e:
                logger.error(f"Error during QA execution: {e}")
                raise CustomException("Failed to execute QA query", e)

        return qa_run

    except Exception as e:
        error_message = CustomException("Failed to make QA retriever", e)
        logger.error(str(error_message))
