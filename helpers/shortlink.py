import base64

async def get_shortlink(link):
    try:
        # Encode the original link to Base64
        encoded_link = base64.urlsafe_b64encode(link.encode()).decode()

        # Construct the safelink URL with the encoded link
        safelink_url = f"https://moxibeatz.fun/p/1.html?url={encoded_link}"
        return safelink_url
        print("Original Link:", original_link)
        print("Encoded Link:", encoded_link)
    except Exception as e:
        logger.error(f"Safelink generation error: {e}")
        return link
        
