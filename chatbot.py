from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

def ask_question(question, vectorstore):
    if not question:
        return "Pose-moi une vraie question 😉"
    
    q_lower = question.lower()
    if q_lower in ["bonjour", "salut", "coucou", "ça va ?"]:
        return "Bonjour ! Pose-moi ta question métier 😊"
    elif "aide" in q_lower:
        return "Je peux t'aider à répondre aux procédures métiers (annulation règlement, déclaration sinistre, etc.)"

    chain = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0),
        retriever=vectorstore.as_retriever()
    )
    return chain.run(question)