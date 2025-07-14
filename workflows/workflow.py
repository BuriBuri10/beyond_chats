import logging
import asyncio
from langgraph.graph import END, START, StateGraph
from langchain_core.runnables.graph import CurveStyle

from workflows.state import NodeState, OutputState
from workflows.graphs.persona.nodes.scraper_node import ScraperNode
from workflows.graphs.persona.nodes.analyzer_node import AnalyzerNode
from workflows.graphs.persona.nodes.formatter_node import FormatterNode
from logs.logging_config import logger


class PersonaWorkflow:
    """
    Defines and compiles the LangGraph workflow for Reddit Persona generation
    """
    def __init__(self):
        logger.info("Initializing PersonaWorkflow...")

        self.scraper_node = ScraperNode()
        self.analyzer_node = AnalyzerNode()
        self.formatter_node = FormatterNode()

        self.graph = self._build_graph()

        logger.info("PersonaWorkflow initialized successfully")

    def _build_graph(self):
        """
        Creates and compiles the LangGraph workflow
        """
        workflow = StateGraph(NodeState, output=OutputState)

        # Define nodes
        workflow.add_node("scraper", self.scraper_node.process)
        workflow.add_node("analyzer", self.analyzer_node.process)
        workflow.add_node("formatter", self.formatter_node.process)

        # Connect the flow
        workflow.add_edge(START, "scraper")
        workflow.add_edge("scraper", "analyzer")
        workflow.add_edge("analyzer", "formatter")
        workflow.add_edge("formatter", END)

        logger.info("Workflow graph defined.")

        return workflow.compile()
    
    async def get_graph_structure(self, use_pyppeteer: bool = True) -> bytes:
        """Get graph structure visual asynchronously"""
        graph = self.graph.get_graph()
        mermaid_string = graph.draw_mermaid(curve_style=CurveStyle.LINEAR)

        if use_pyppeteer:
            try:
                from langchain_core.runnables.graph_mermaid import _render_mermaid_using_pyppeteer

                img_bytes = await _render_mermaid_using_pyppeteer(mermaid_string)
                return img_bytes
            except ImportError:
                logger.warning(
                    f"Pyppeteer is not installed. To enable browser-based rendering, run:\n\n    pip install pyppeteer\n"
                )
            except Exception as e:
                logger.warning(
                    f"Pyppeteer render failed due to unexpectedd error:\n{e}\n"
                    "</Falling back to Local Mermaid Rendereing>"
                )

        # Fallback: Locally Rendering Mermaid graph without using pyppeteer
        try:
            img_bytes = self.graph.get_graph().draw_mermaid_png(curve_style=CurveStyle.LINEAR)
            logger.info("Graph saved as -- graph_structure.png")
            return img_bytes
        except Exception as e:
            logger.error(f"Local Mermaid Rendering failed:\n{e}")
            raise

    async def extract_username(url: str) -> str:
        """
        Extracts the Reddit username from a profile URL.
        Example: https://www.reddit.com/user/kojied/ -> "kojied"
        """
        url = url.rstrip("/")
        parts = url.split("/")
        if "user" in parts:
            index = parts.index("user")
            if index + 1 < len(parts):
                return parts[index + 1]
        raise ValueError("Invalid Reddit user URL format")

    async def run(self, username: str) -> dict:
        """
        Run the persona workflow asynchronously.

        Args:
            username (str): Reddit username to analyze.

        Returns:
            dict: OutputState containing the final persona summary.
        """
        try:
            logger.info(f"Running workflow for user: {username}")
            input_state = {"username": username}
            result = await self.graph.ainvoke(input_state)
            return result
        except Exception as e:
            logger.error(f"Workflow run failed: {e}")
            return {"error": str(e)}
        

if __name__ == "__main__":
    async def main():
        reddit_url = input("Enter the Reddit profile URL (eg - https://www.reddit.com/user/kojied/): ").strip()
        logger.info(f"Received URL: {reddit_url}")
        
        try:
            username = await PersonaWorkflow.extract_username(reddit_url)
        except Exception as e:
            print(f"Error extracting username: {e}")
            return

        workflow = PersonaWorkflow()
        print(f"Running persona workflow for user: {username}")
        result = await workflow.run(username=username)

        if result is None:
            print("Workflow returned no result")
            return

        if isinstance(result, dict):
            if "response" in result:
                print("\nGenerated Persona:\n")
                print(result["response"])
            elif "error" in result:
                print("\nWorkflow failed:")
                print(result["error"])
            else:
                print("\nWorkflow failed: Unknown result structure")
                print(result)
        else:
            print("\nUnexpected result type:")
            print(result)

        # Saving graph's structure
        try:
            graph_bytes = await workflow.get_graph_structure()
            with open("graph_structure.png", "wb") as f:
                f.write(graph_bytes)
            logger.info("Saved graph's structure as graph_structure.png")
        except Exception as e:
            logger.error(f"Couldn't save graph structure: {e}")

    asyncio.run(main())