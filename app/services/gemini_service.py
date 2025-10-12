import os
import google.generativeai as genai
from typing import List, Dict, Optional
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-pro')

        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
            return

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

        # Initialize conversation history
        self.conversation_history = []

        # Study-focused system prompt
        self.system_prompt = """
        You are StudyBot, an AI assistant specifically designed to help high school students with their academics and personal development. Your role is to:

        1. Provide study tips, techniques, and learning strategies
        2. Help with time management and organization
        3. Offer motivation and encouragement
        4. Assist with understanding academic concepts (but don't do homework for them)
        5. Guide students in developing good study habits
        6. Help with stress management and academic pressure

        Keep your responses:
        - Encouraging and positive
        - Age-appropriate for high school students
        - Focused on learning and growth
        - Practical and actionable
        - Concise but comprehensive (aim for 2-4 sentences unless more detail is needed)

        Always encourage students to think critically and learn rather than just providing direct answers to homework questions.
        """

    def is_configured(self) -> bool:
        """Check if the service is properly configured"""
        return bool(self.api_key and hasattr(self, 'model'))

    def generate_response(self, user_message: str, conversation_context: Optional[List[Dict]] = None) -> str:
        """
        Generate a response using GEMINI API

        Args:
            user_message: The user's input message
            conversation_context: Previous conversation history for context

        Returns:
            Generated response string
        """
        if not self.is_configured():
            return "I'm sorry, but I'm not properly configured right now. Please check that the GEMINI API key is set correctly."

        try:
            # Build conversation context
            prompt_parts = [self.system_prompt]

            # Add conversation history for context (last 5 exchanges)
            if conversation_context:
                recent_context = conversation_context[-10:]  # Last 10 messages (5 exchanges)
                for msg in recent_context:
                    if msg.get('role') == 'user':
                        prompt_parts.append(f"Student: {msg.get('content', '')}")
                    elif msg.get('role') == 'assistant':
                        prompt_parts.append(f"StudyBot: {msg.get('content', '')}")

            # Add current user message
            prompt_parts.append(f"Student: {user_message}")
            prompt_parts.append("StudyBot:")

            full_prompt = "\n\n".join(prompt_parts)

            # Generate response
            response = self.model.generate_content(full_prompt)

            if response and response.text:
                return response.text.strip()
            else:
                return "I'm having trouble generating a response right now. Could you try rephrasing your question?"

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I'm experiencing some technical difficulties. Please try again in a moment."

    def get_study_tips(self, subject: Optional[str] = None) -> str:
        """Get general study tips or subject-specific tips"""
        if subject:
            prompt = f"Provide 3-4 specific study tips for high school {subject}. Make them practical and actionable."
        else:
            prompt = "Provide 4-5 general study tips that would help any high school student improve their learning."

        return self.generate_response(prompt)

    def get_motivation_message(self, context: Optional[str] = None) -> str:
        """Generate a motivational message"""
        if context:
            prompt = f"Provide an encouraging and motivational message for a high school student who is {context}. Keep it uplifting and practical."
        else:
            prompt = "Provide an encouraging and motivational message for high school students about the importance of perseverance in their studies."

        return self.generate_response(prompt)

    def help_with_time_management(self, specific_challenge: Optional[str] = None) -> str:
        """Provide time management advice"""
        if specific_challenge:
            prompt = f"Help a high school student with this time management challenge: {specific_challenge}. Provide practical, actionable advice."
        else:
            prompt = "Provide practical time management tips specifically for high school students balancing multiple subjects and activities."

        return self.generate_response(prompt)

    def explain_study_technique(self, technique: str) -> str:
        """Explain a specific study technique"""
        prompt = f"Explain the {technique} study method to a high school student. Include how to use it effectively and what subjects it works best for."
        return self.generate_response(prompt)

# Global instance
gemini_service = GeminiService()