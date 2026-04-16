from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from app import db
from models import Conversation, Message, Listing

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/listing/<int:listing_id>/contact', methods=['POST'])
@login_required
def contact_seller(listing_id):
    listing = Listing.query.get_or_404(listing_id)

    if listing.user_id == current_user.id:
        flash('You cannot contact yourself.', 'warning')
        return redirect(url_for('listings.detail', listing_id=listing_id))

    # Check if conversation already exists
    existing = Conversation.query.filter_by(
        listing_id=listing_id,
        buyer_id=current_user.id
    ).first()

    if existing:
        flash('You already have an open conversation for this listing.', 'info')
        return redirect(url_for('messages.chat', conversation_id=existing.id))

    body = request.form.get('body', '').strip()
    if not body:
        flash('Message cannot be empty.', 'danger')
        return redirect(url_for('listings.detail', listing_id=listing_id))

    conv = Conversation(
        listing_id=listing_id,
        buyer_id=current_user.id,
        seller_id=listing.user_id
    )
    db.session.add(conv)
    db.session.flush()

    msg = Message(conversation_id=conv.id, sender_id=current_user.id, body=body)
    db.session.add(msg)
    db.session.commit()

    flash('Your request has been sent!', 'success')
    return redirect(url_for('messages.inbox'))


@messages_bp.route('/messages')
@login_required
def inbox():
    buying = Conversation.query.filter_by(buyer_id=current_user.id).order_by(Conversation.created_at.desc()).all()
    selling = Conversation.query.filter_by(seller_id=current_user.id).order_by(Conversation.created_at.desc()).all()
    return render_template('messages_inbox.html', buying=buying, selling=selling)


@messages_bp.route('/messages/<int:conversation_id>', methods=['GET', 'POST'])
@login_required
def chat(conversation_id):
    conv = Conversation.query.get_or_404(conversation_id)

    if current_user.id not in [conv.buyer_id, conv.seller_id]:
        abort(403)

    if request.method == 'POST':
        if conv.status != 'accepted':
            flash('The conversation is not active yet.', 'warning')
            return redirect(url_for('messages.chat', conversation_id=conversation_id))

        body = request.form.get('body', '').strip()
        if body:
            msg = Message(conversation_id=conv.id, sender_id=current_user.id, body=body)
            db.session.add(msg)
            db.session.commit()

        return redirect(url_for('messages.chat', conversation_id=conversation_id))

    return render_template('messages_chat.html', conv=conv)


@messages_bp.route('/messages/<int:conversation_id>/accept', methods=['POST'])
@login_required
def accept(conversation_id):
    conv = Conversation.query.get_or_404(conversation_id)
    if current_user.id != conv.seller_id:
        abort(403)
    conv.status = 'accepted'
    db.session.commit()
    flash('Request accepted!', 'success')
    return redirect(url_for('messages.chat', conversation_id=conversation_id))


@messages_bp.route('/messages/<int:conversation_id>/reject', methods=['POST'])
@login_required
def reject(conversation_id):
    conv = Conversation.query.get_or_404(conversation_id)
    if current_user.id != conv.seller_id:
        abort(403)
    conv.status = 'rejected'
    db.session.commit()
    flash('Request rejected.', 'info')
    return redirect(url_for('messages.inbox'))