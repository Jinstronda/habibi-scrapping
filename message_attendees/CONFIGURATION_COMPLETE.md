# ✅ Configuration Complete!

All UI element selectors have been discovered and configured.

---

## 📋 Discovered Selectors

### From `hierarchy.xml` (Main attendees screen)
```python
SEARCH_ICON_SELECTOR = {"resourceId": "com.swapcard.apps.android.adipec:id/action_search"}
SEARCH_RESULT_SELECTOR = {"resourceId": "com.swapcard.apps.android.adipec:id/content_layout"}
```

### From `search_screen.xml` (After clicking search)
```python
SEARCH_INPUT_SELECTOR = {"resourceId": "com.swapcard.apps.android.adipec:id/search_src_text"}
```

### From `profile_screen.xml` (Person's profile)
```python
DIRECT_MESSAGE_BUTTON = {"description": "Direct Message"}  # Using content-desc
```

### From `message_screen.xml` (Message conversation)
```python
MESSAGE_INPUT_SELECTOR = {"resourceId": "com.swapcard.apps.android.adipec:id/edit_text_message"}
SEND_BUTTON_SELECTOR = {"resourceId": "com.swapcard.apps.android.adipec:id/btn_send"}
```

---

## 🧪 Testing

### Quick Test (Single Message)
```bash
python test_single_message.py
```

This will test the complete flow with Aaron Yap:
1. Click search icon
2. Type "Aaron Yap"
3. Click search result
4. Click "Direct Message"
5. Type "Looking forward to the event"
6. Send message
7. Return to search screen

Watch for ✓ or ❌ at each step to verify everything works.

---

### Full Run (5 Test Names)
```bash
python main.py
```

This will message all 5 people in `test_list.txt`:
- Aaron Yap
- Roy Yap
- Lin Lin Yap
- Gary Yap
- Kristel Yap

Check results:
```bash
python check_db.py
```

---

## 📊 Expected Output

### Success Messages
```
✓ Message sent to Aaron Yap
✓ Message sent to Roy Yap
✓ Message sent to Lin Lin Yap
✓ Message sent to Gary Yap
✓ Message sent to Kristel Yap

Complete! Sent: 5, Skipped: 0, Failed: 0
```

### Database Check
```bash
python check_db.py
```
Should show:
- Total messages: 5
- Successful: 5
- Failed: 0
- Recent messages with timestamps

---

## 🎯 Next Steps

### 1. Test with Single Message
```bash
python test_single_message.py
```

### 2. If successful, run full test batch
```bash
python main.py
```

### 3. Scale to full database
Once validated with 5 test names, edit `config.py`:
```python
USE_TEST_LIST = False  # Use full scraper_attendees database
```

Then run again:
```bash
python main.py
```

---

## 🔧 Customization

### Change Message
Edit `config.py`:
```python
DEFAULT_MESSAGE = "Your custom message here"
```

### Adjust Timeouts
If experiencing failures, increase timeouts in `config.py`:
```python
SEARCH_WAIT = 1.0  # Increase if search results load slowly
PAGE_LOAD_TIMEOUT = 1.5  # Increase if profiles load slowly
MESSAGE_SENT_WAIT = 0.8  # Increase if messages send slowly
```

---

## 🚨 Troubleshooting

### "Failed to click search icon"
- Check that you're on the Attendees tab
- Verify SEARCH_ICON_SELECTOR in config.py

### "Search result not found"
- Name might be slightly different in app
- Check SEARCH_RESULT_SELECTOR
- Increase SEARCH_WAIT timeout

### "Direct Message button not found"
- Person might not have direct messaging enabled
- Check DIRECT_MESSAGE_BUTTON selector
- Button might have different text/description

### "Failed to send message"
- Check MESSAGE_INPUT_SELECTOR
- Check SEND_BUTTON_SELECTOR
- Increase MESSAGE_SENT_WAIT timeout

---

## ✅ Ready to Go!

All selectors are configured. The bot is ready to use!

```bash
# Quick test
python test_single_message.py

# Full run
python main.py
```

Good luck! 🚀

