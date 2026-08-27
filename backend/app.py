from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from rag_pipeline import RAGPipeline


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="Enterprise AI Knowledge OS",
    description=(
        "AI-powered enterprise knowledge retrieval "
        "and grounded question answering system"
    ),
    version="1.1.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# RAG PIPELINE
# ============================================================

pipeline = None


@app.on_event("startup")
def startup_event():

    global pipeline

    print("=" * 60)
    print("ENTERPRISE AI KNOWLEDGE OS")
    print("Starting backend...")
    print("=" * 60)

    try:

        pipeline = RAGPipeline()

        print("RAG Pipeline ready.")
        print("Backend startup complete.")

    except Exception as error:

        print("=" * 60)
        print("BACKEND STARTUP ERROR")
        print(error); import traceback; traceback.print_exc()
        print("=" * 60)

        pipeline = None


# ============================================================
# REQUEST MODEL
# ============================================================

class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
    )


# ============================================================
# SOURCE MODEL
# ============================================================

class Source(BaseModel):

    document: str

    page: int | None = None

    score: float

    chunk_id: str

    hybrid_score: float = 0.0

    reranker_score: float = 0.0


# ============================================================
# CONFIDENCE MODEL
# ============================================================

class Confidence(BaseModel):

    score: float = 0.0

    percentage: float = 0.0

    level: str = "LOW"

    grounded: bool = False

    best_evidence: float = 0.0

    average_evidence: float = 0.0

    evidence_coverage: float = 0.0

    reason: str = ""


# ============================================================
# RESPONSE MODEL
# ============================================================

class QuestionResponse(BaseModel):

    question: str

    answer: str

    sources: List[Source]

    confidence: Confidence


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    if pipeline is None:

        return {
            "status": "starting",
            "service": "Enterprise AI Knowledge OS",
        }

    vector_count = 0

    try:

        vector_count = (
            pipeline.vector_store.count()
        )

    except Exception:

        pass

    return {

        "status": "healthy",

        "service": (
            "Enterprise AI Knowledge OS"
        ),

        "vectors": vector_count,

        "rag": True,

        "hybrid_search": (
            pipeline.hybrid_search is not None
        ),

        "reranker": (
            pipeline.reranker is not None
        ),

        "confidence_engine": (
            pipeline.confidence_engine is not None
        ),

    }


# ============================================================
# ASK QUESTION
# ============================================================

@app.post(
    "/api/ask",
    response_model=QuestionResponse,
)
def ask_question(
    request: QuestionRequest,
):

    if pipeline is None:

        raise HTTPException(
            status_code=503,
            detail=(
                "RAG pipeline is not ready. "
                "Check backend startup logs."
            ),
        )

    try:

        # ====================================================
        # USE THE COMPLETE RAG PIPELINE
        # ====================================================

        results = pipeline.retrieve(
            request.question,
            top_k=request.top_k,
        )

        # ====================================================
        # CONFIDENCE
        # ====================================================

        confidence = (
            pipeline.confidence_engine.calculate(
                results
            )
        )

        # ====================================================
        # NO EVIDENCE
        # ====================================================

        if not results:

            return QuestionResponse(

                question=request.question,

                answer=(
                    "I could not find relevant "
                    "information in the knowledge base."
                ),

                sources=[],

                confidence=confidence,
            )

        # ====================================================
        # LOW CONFIDENCE
        # ====================================================

        if not confidence["grounded"]:

            sources = []

            for result in results:

                sources.append(
                    Source(

                        document=result.get(
                            "document",
                            "Unknown",
                        ),

                        page=result.get(
                            "page"
                        ),

                        score=float(
                            result.get(
                                "score",
                                0.0,
                            )
                        ),

                        chunk_id=str(
                            result.get(
                                "chunk_id",
                                "unknown",
                            )
                        ),

                        hybrid_score=float(
                            result.get(
                                "hybrid_score",
                                0.0,
                            )
                        ),

                        reranker_score=float(
                            result.get(
                                "reranker_score",
                                0.0,
                            )
                        ),
                    )
                )

            return QuestionResponse(

                question=request.question,

                answer=(
                    "I could not find enough reliable "
                    "evidence in the enterprise knowledge "
                    "base to answer this question confidently."
                ),

                sources=sources,

                confidence=confidence,
            )

        # ====================================================
        # BUILD CONTEXT
        # ====================================================

        context = pipeline.build_context(
            results
        )

        # ====================================================
        # GENERATE GROUNDED ANSWER
        # ====================================================

        answer = pipeline.llm.generate(

            question=request.question,

            context=context,
        )

        # ====================================================
        # SOURCES
        # ====================================================

        sources = []

        for result in results:

            sources.append(
                Source(

                    document=result.get(
                        "document",
                        "Unknown",
                    ),

                    page=result.get(
                        "page"
                    ),

                    score=float(
                        result.get(
                            "score",
                            0.0,
                        )
                    ),

                    chunk_id=str(
                        result.get(
                            "chunk_id",
                            "unknown",
                        )
                    ),

                    hybrid_score=float(
                        result.get(
                            "hybrid_score",
                            0.0,
                        )
                    ),

                    reranker_score=float(
                        result.get(
                            "reranker_score",
                            0.0,
                        )
                    ),
                )
            )

        # ====================================================
        # RESPONSE
        # ====================================================

        return QuestionResponse(

            question=request.question,

            answer=answer,

            sources=sources,

            confidence=confidence,
        )

    except Exception as error:

        print("=" * 60)
        print("API ERROR")
        print(error); import traceback; traceback.print_exc()
        print("=" * 60)

        raise HTTPException(

            status_code=500,

            detail=str(error),
        )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {

        "service": (
            "Enterprise AI Knowledge OS"
        ),

        "status": "running",

        "version": "1.1.0",

        "endpoints": {

            "health": "/health",

            "ask": "/api/ask",

            "docs": "/docs",

        },
    }

from document_api import router as document_router

app.include_router(document_router)

from fastapi import HTTPException
from pydantic import BaseModel, Field

from agent.orchestrator import AgentOrchestrator
from agent.memory import InvestigationMemory


class AgentRequest(BaseModel):
    objective: str = Field(..., min_length=5, max_length=2000)
    top_k: int = Field(default=8, ge=1, le=15)


agent_orchestrator = None

investigation_memory = InvestigationMemory()


@app.on_event("startup")
def startup_agent():
    global agent_orchestrator

    if pipeline is not None:
        agent_orchestrator = AgentOrchestrator(pipeline)
        print("Agent Orchestrator ready.")


@app.post("/api/agent/research")
def research_agent_endpoint(request: AgentRequest):

    if pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="RAG pipeline is not ready."
        )

    try:

        global agent_orchestrator

        if agent_orchestrator is None:
            agent_orchestrator = AgentOrchestrator(
                pipeline
            )

        result = agent_orchestrator.run(
            request.objective
        )

        return result

    except Exception as error:

        print("=" * 60)
        print("AGENT ERROR")
        print(error); import traceback; traceback.print_exc()
        print("=" * 60)

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@app.get("/api/agent/history")
def get_agent_history():

    try:

        history = investigation_memory.latest(
            limit=50
        )

        return {
            "count": len(history),
            "history": history,
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.get("/api/agent/history/{investigation_id}")
def get_agent_investigation(
    investigation_id: int
):

    try:

        history = investigation_memory.load()

        for investigation in history:

            if investigation.get("id") == investigation_id:

                return investigation

        raise HTTPException(
            status_code=404,
            detail="Investigation not found."
        )

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


from document_summary_api import router as document_summary_router
app.include_router(document_summary_router)
