from flask import Blueprint, request, jsonify, session, render_template
from app.services.gemini_service import gemini_service
from app.services.vector_service import vector_service
import uuid
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)

def get_or_create_user_id():
    """Get or create a unique user ID for the session"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return session['user_id']

def get_conversation_history():
    """Get conversation history from session"""
    if 'conversation_history' not in session:
        session['conversation_history'] = []
    return session['conversation_history']

def add_to_conversation_history(role, content):
    """Add a message to conversation history"""
    conversation_history = get_conversation_history()
    conversation_history.append({
        'role': role,
        'content': content,
        'timestamp': datetime.now().isoformat()
    })

    # Keep only the last 20 messages to prevent session from growing too large
    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]

    session['conversation_history'] = conversation_history

@chat_bp.route('/chat')
def chat_page():
    """Render the chat page"""
    return render_template('chat.html')

@chat_bp.route('/api/chat', methods=['POST'])
def chat_api():
    """
    Main chat API endpoint
    Handles user messages and returns AI responses
    """
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400

        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400

        # Get user ID and conversation history
        user_id = get_or_create_user_id()
        conversation_history = get_conversation_history()

        # Add user message to conversation history
        add_to_conversation_history('user', user_message)

        # Get relevant past conversations for context
        relevant_conversations = vector_service.get_relevant_conversations(
            user_id=user_id,
            query=user_message,
            limit=3
        )

        # Generate AI response using GEMINI
        if gemini_service.is_configured():
            ai_response = gemini_service.generate_response(
                user_message=user_message,
                conversation_context=conversation_history
            )
        else:
            ai_response = "I'm sorry, but I'm not properly configured right now. Please make sure the GEMINI API key is set up correctly."

        # Add AI response to conversation history
        add_to_conversation_history('assistant', ai_response)

        # Store conversation in vector database for future context
        vector_service.store_conversation(
            user_id=user_id,
            user_message=user_message,
            bot_response=ai_response,
            conversation_context={'session_id': session.get('_id', 'unknown')}
        )

        # Return response
        return jsonify({
            'response': ai_response,
            'timestamp': datetime.now().isoformat(),
            'conversation_id': len(conversation_history) // 2  # Rough conversation turn count
        })

    except Exception as e:
        logger.error(f"Error in chat API: {str(e)}")
        return jsonify({
            'error': 'An error occurred while processing your message. Please try again.',
            'timestamp': datetime.now().isoformat()
        }), 500

@chat_bp.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    """Get conversation history for the current session"""
    try:
        conversation_history = get_conversation_history()

        # Format history for frontend
        formatted_history = []
        for i in range(0, len(conversation_history), 2):
            if i + 1 < len(conversation_history):
                user_msg = conversation_history[i]
                bot_msg = conversation_history[i + 1]

                formatted_history.append({
                    'id': i // 2,
                    'user_message': user_msg['content'],
                    'bot_response': bot_msg['content'],
                    'timestamp': user_msg['timestamp'],
                    'preview': user_msg['content'][:50] + '...' if len(user_msg['content']) > 50 else user_msg['content']
                })

        return jsonify({
            'history': formatted_history[-10:],  # Last 10 conversations
            'total_conversations': len(formatted_history)
        })

    except Exception as e:
        logger.error(f"Error getting chat history: {str(e)}")
        return jsonify({'error': 'Failed to retrieve chat history'}), 500

@chat_bp.route('/api/chat/quick-response', methods=['POST'])
def quick_response():
    """
    Handle quick response buttons/suggestions
    """
    try:
        data = request.get_json()
        if not data or 'type' not in data:
            return jsonify({'error': 'Response type is required'}), 400

        response_type = data['type']
        user_id = get_or_create_user_id()

        # Generate appropriate response based on type
        if response_type == 'study_tips':
            subject = data.get('subject')
            response = gemini_service.get_study_tips(subject)
        elif response_type == 'motivation':
            context = data.get('context')
            response = gemini_service.get_motivation_message(context)
        elif response_type == 'time_management':
            challenge = data.get('challenge')
            response = gemini_service.help_with_time_management(challenge)
        elif response_type == 'study_technique':
            technique = data.get('technique', 'Pomodoro Technique')
            response = gemini_service.explain_study_technique(technique)
        else:
            response = "I'm not sure how to help with that. Could you ask me a specific question?"

        # Store this interaction
        user_message = f"Quick request: {response_type}"
        add_to_conversation_history('user', user_message)
        add_to_conversation_history('assistant', response)

        vector_service.store_conversation(
            user_id=user_id,
            user_message=user_message,
            bot_response=response,
            conversation_context={'type': 'quick_response', 'response_type': response_type}
        )

        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'type': response_type
        })

    except Exception as e:
        logger.error(f"Error in quick response: {str(e)}")
        return jsonify({'error': 'Failed to generate quick response'}), 500

@chat_bp.route('/api/chat/search-knowledge', methods=['POST'])
def search_knowledge():
    """
    Search stored knowledge base for relevant information
    """
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Search query is required'}), 400

        query = data['query'].strip()
        category = data.get('category')
        limit = min(data.get('limit', 5), 10)  # Max 10 results

        # Search knowledge base
        knowledge_items = vector_service.search_study_knowledge(
            query=query,
            category=category,
            limit=limit
        )

        # Format results
        formatted_results = []
        for item in knowledge_items:
            formatted_results.append({
                'title': item['metadata'].get('title', 'Untitled'),
                'content': item['content'],
                'category': item['metadata'].get('category', 'general'),
                'similarity': round(item['similarity'], 3),
                'tags': item['metadata'].get('tags', '').split(',') if item['metadata'].get('tags') else []
            })

        return jsonify({
            'results': formatted_results,
            'query': query,
            'total_found': len(formatted_results)
        })

    except Exception as e:
        logger.error(f"Error searching knowledge: {str(e)}")
        return jsonify({'error': 'Failed to search knowledge base'}), 500

@chat_bp.route('/api/chat/clear-history', methods=['POST'])
def clear_chat_history():
    """Clear conversation history for the current session"""
    try:
        session['conversation_history'] = []
        return jsonify({'message': 'Chat history cleared successfully'})

    except Exception as e:
        logger.error(f"Error clearing chat history: {str(e)}")
        return jsonify({'error': 'Failed to clear chat history'}), 500

@chat_bp.route('/api/chat/status', methods=['GET'])
def chat_status():
    """Get the status of chat services"""
    try:
        status = {
            'gemini_configured': gemini_service.is_configured(),
            'vector_db_available': hasattr(vector_service, 'client'),
            'session_active': 'user_id' in session,
            'conversation_count': len(get_conversation_history()) // 2
        }

        return jsonify(status)

    except Exception as e:
        logger.error(f"Error getting chat status: {str(e)}")
        return jsonify({'error': 'Failed to get chat status'}), 500