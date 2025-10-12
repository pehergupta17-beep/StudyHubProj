#!/usr/bin/env python3
"""
Initialize the knowledge base with study-related content
Run this script after setting up the environment to populate the vector database
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.vector_service import vector_service

def initialize_knowledge_base():
    """Initialize the vector database with comprehensive study knowledge"""

    print("🚀 Initializing StudyHub Knowledge Base...")

    # Study Techniques
    study_techniques = [
        {
            "title": "Active Recall Method",
            "content": "Active recall involves testing yourself on information rather than passively reviewing it. Close your textbook and try to remember key concepts, then check your accuracy. This method strengthens neural pathways and identifies knowledge gaps. Use flashcards, practice tests, or explain concepts aloud without looking at notes.",
            "category": "study_techniques",
            "tags": ["memory", "retention", "testing", "flashcards"]
        },
        {
            "title": "Spaced Repetition System",
            "content": "Review material at increasing intervals: 1 day, 3 days, 1 week, 2 weeks, 1 month. This leverages the forgetting curve to maximize long-term retention with minimal effort. Apps like Anki or manual scheduling can help implement this system effectively.",
            "category": "study_techniques",
            "tags": ["memory", "retention", "scheduling", "long-term"]
        },
        {
            "title": "Feynman Technique",
            "content": "Explain concepts in simple terms as if teaching a child. This reveals gaps in understanding and forces you to break down complex ideas. Steps: 1) Choose a concept, 2) Explain it simply, 3) Identify gaps, 4) Review and simplify further.",
            "category": "study_techniques",
            "tags": ["understanding", "explanation", "simplification"]
        },
        {
            "title": "Mind Mapping",
            "content": "Create visual representations of information using central topics with branching subtopics. This technique helps with visual learners and shows relationships between concepts. Use colors, images, and keywords to make maps memorable.",
            "category": "study_techniques",
            "tags": ["visual", "organization", "relationships", "creativity"]
        },
        {
            "title": "Cornell Note-Taking System",
            "content": "Divide your page into three sections: notes (main area), cues (left margin), and summary (bottom). During class, take notes in the main area. After class, write questions/keywords in the cue section and summarize at the bottom.",
            "category": "study_techniques",
            "tags": ["notes", "organization", "review", "structure"]
        }
    ]

    # Time Management
    time_management_tips = [
        {
            "title": "Pomodoro Technique for Students",
            "content": "Work in 25-minute focused sessions followed by 5-minute breaks. After 4 pomodoros, take a longer 15-30 minute break. This prevents mental fatigue and maintains high concentration. Remove all distractions during work sessions.",
            "category": "time_management",
            "tags": ["focus", "breaks", "productivity", "concentration"]
        },
        {
            "title": "Time Blocking Method",
            "content": "Schedule specific time blocks for different subjects or activities. Assign each block a specific purpose (math homework, reading, review). This prevents multitasking and ensures all subjects get adequate attention.",
            "category": "time_management",
            "tags": ["scheduling", "planning", "organization", "focus"]
        },
        {
            "title": "Eisenhower Matrix for Students",
            "content": "Categorize tasks by urgency and importance: 1) Urgent + Important (do first), 2) Important + Not Urgent (schedule), 3) Urgent + Not Important (delegate/minimize), 4) Neither (eliminate). Focus most energy on quadrant 2.",
            "category": "time_management",
            "tags": ["prioritization", "planning", "urgency", "importance"]
        },
        {
            "title": "Backward Planning",
            "content": "Start with your deadline and work backwards to create milestones. For a research paper due in 4 weeks: Week 4 (final draft), Week 3 (first draft), Week 2 (research), Week 1 (outline). Build in buffer time for unexpected challenges.",
            "category": "time_management",
            "tags": ["planning", "deadlines", "milestones", "projects"]
        }
    ]

    # Motivation and Mindset
    motivation_content = [
        {
            "title": "Growth Mindset for Learning",
            "content": "Believe that abilities can be developed through effort and strategy. View challenges as opportunities to grow, not threats to your intelligence. Replace 'I can't do this' with 'I can't do this yet.' Embrace mistakes as learning opportunities.",
            "category": "motivation",
            "tags": ["mindset", "growth", "resilience", "learning"]
        },
        {
            "title": "Setting SMART Academic Goals",
            "content": "Create Specific, Measurable, Achievable, Relevant, Time-bound goals. Instead of 'improve math,' try 'increase algebra test scores from 70% to 85% by the end of the semester through daily practice and weekly tutoring sessions.'",
            "category": "motivation",
            "tags": ["goals", "planning", "achievement", "specific"]
        },
        {
            "title": "Dealing with Academic Stress",
            "content": "Recognize stress signals early. Use deep breathing, regular exercise, and adequate sleep. Break overwhelming tasks into smaller steps. Talk to teachers, counselors, or trusted adults when feeling overwhelmed. Remember that asking for help is a sign of strength.",
            "category": "motivation",
            "tags": ["stress", "wellness", "support", "health"]
        },
        {
            "title": "Building Study Confidence",
            "content": "Start with easier topics to build momentum. Celebrate small wins and track progress visually. Form study groups with supportive peers. Prepare thoroughly for tests to reduce anxiety. Remember that confidence comes from competence, which comes from practice.",
            "category": "motivation",
            "tags": ["confidence", "preparation", "support", "practice"]
        }
    ]

    # Subject-Specific Tips
    subject_tips = [
        {
            "title": "Mathematics Study Strategies",
            "content": "Practice problems daily, not just before tests. Work through problems step-by-step without skipping steps. Keep a formula sheet with explanations. Form study groups to explain concepts to others. Don't just memorize procedures - understand the why behind each step.",
            "category": "subject_specific",
            "tags": ["math", "practice", "understanding", "formulas"]
        },
        {
            "title": "Science Learning Techniques",
            "content": "Connect concepts to real-world examples. Use diagrams and flowcharts for processes. Create concept maps showing relationships. Practice lab techniques and understand the scientific method. Read science news to see concepts in action.",
            "category": "subject_specific",
            "tags": ["science", "concepts", "real-world", "diagrams"]
        },
        {
            "title": "History and Social Studies Methods",
            "content": "Create timelines to understand chronological relationships. Connect events to causes and effects. Use mnemonics for dates and facts. Read primary sources when possible. Discuss topics with others to gain different perspectives.",
            "category": "subject_specific",
            "tags": ["history", "timeline", "connections", "sources"]
        },
        {
            "title": "Language Arts and Reading",
            "content": "Read actively by taking notes and asking questions. Practice writing regularly, not just for assignments. Build vocabulary through context and word roots. Join book clubs or discussion groups. Read diverse genres to improve comprehension skills.",
            "category": "subject_specific",
            "tags": ["reading", "writing", "vocabulary", "discussion"]
        }
    ]

    # Test Taking Strategies
    test_strategies = [
        {
            "title": "Test Preparation Strategies",
            "content": "Start reviewing at least a week before the test. Create a study schedule covering all topics. Use practice tests to identify weak areas. Get adequate sleep before test day. Review key concepts the morning of the test, but avoid cramming new material.",
            "category": "test_taking",
            "tags": ["preparation", "review", "practice", "sleep"]
        },
        {
            "title": "During Test Strategies",
            "content": "Read all instructions carefully. Budget your time based on point values. Answer easy questions first to build confidence. For multiple choice, eliminate obviously wrong answers. Show all work on math problems even if not required.",
            "category": "test_taking",
            "tags": ["instructions", "time", "strategy", "confidence"]
        },
        {
            "title": "Managing Test Anxiety",
            "content": "Practice relaxation techniques like deep breathing. Arrive early but not too early to avoid nervous energy. Bring necessary supplies to reduce stress. Use positive self-talk and remind yourself of your preparation. Focus on the process, not the outcome.",
            "category": "test_taking",
            "tags": ["anxiety", "relaxation", "preparation", "mindset"]
        }
    ]

    # Combine all knowledge
    all_knowledge = (study_techniques + time_management_tips + motivation_content +
                    subject_tips + test_strategies)

    # Store all knowledge in the vector database
    success_count = 0
    for item in all_knowledge:
        if vector_service.store_study_knowledge(
            title=item["title"],
            content=item["content"],
            category=item["category"],
            tags=item.get("tags", [])
        ):
            success_count += 1
            print(f"✅ Added: {item['title']}")
        else:
            print(f"❌ Failed to add: {item['title']}")

    print(f"\n🎉 Knowledge base initialization complete!")
    print(f"📚 Successfully added {success_count}/{len(all_knowledge)} knowledge items")

    if success_count < len(all_knowledge):
        print("⚠️  Some items failed to add. Check the logs for details.")

    return success_count == len(all_knowledge)

if __name__ == "__main__":
    try:
        success = initialize_knowledge_base()
        if success:
            print("\n✨ Your StudyHub AI assistant is now ready with comprehensive study knowledge!")
            print("💡 Don't forget to set your GEMINI_API_KEY in the .env file for full AI capabilities.")
        else:
            print("\n⚠️  Initialization completed with some errors. Please check the configuration.")

    except Exception as e:
        print(f"\n❌ Error during initialization: {str(e)}")
        print("Please check your environment setup and try again.")
        sys.exit(1)