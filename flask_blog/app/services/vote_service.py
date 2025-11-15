from app.models import Vote, Post
from app.extensions import blog_db


class VoteService:
    @staticmethod
    def cast_vote(user_id, post_id, value):
        
        # Check if user already voted
        existing_vote = Vote.query.filter_by(user_id=user_id, post_id=post_id).first()
        if existing_vote:
            # Update existing vote
            existing_vote.value = value
        else:
            # Create new vote
            new_vote = Vote(user_id=user_id, post_id=post_id, value=value)
            blog_db.session.add(new_vote)

        blog_db.session.commit()

        # Recalculate post score
        post = Post.query.get(post_id)
        post.votes = sum(v.value for v in post.votes_rel)
        blog_db.session.commit()
        return post
