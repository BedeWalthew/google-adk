# Weather Assistant Frontend

Modern Next.js chat application for interacting with the Google ADK Weather Assistant.

## Features

- 💬 Real-time chat interface
- 🎨 Modern, responsive UI with Tailwind CSS
- ⚡ Fast and optimized with Next.js 14
- 🌈 Beautiful gradient design
- 📱 Mobile-friendly
- ♿ Accessible components

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

```bash
# Copy the example file
cp .env.local.example .env.local

# Edit .env.local if needed (default points to localhost:8000)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

The app will start at: `http://localhost:3000`

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page
│   └── globals.css         # Global styles
├── components/
│   ├── ChatInterface.tsx   # Main chat container
│   ├── MessageList.tsx     # Message display
│   └── InputBox.tsx        # Input component
├── lib/
│   └── api.ts              # API client
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.js
```

## Usage

1. Make sure the backend server is running at `http://localhost:8000`
2. Start the frontend with `npm run dev`
3. Open `http://localhost:3000` in your browser
4. Start chatting with the weather assistant!

## Example Queries

- "What's the weather in Paris?"
- "Will it rain in London tomorrow?"
- "Show me the forecast for New York"
- "What's the temperature in Tokyo?"
- "Is it cold in Moscow right now?"

## Components

### ChatInterface
Main container that manages:
- Message state
- API communication
- Conversation flow
- Error handling

### MessageList
Displays:
- User messages (right-aligned, indigo)
- Agent messages (left-aligned, white)
- Loading indicator
- Timestamps

### InputBox
Handles:
- Text input
- Send button
- Enter key submission
- Character limits
- Disabled states

## Styling

Built with Tailwind CSS featuring:
- Gradient backgrounds
- Smooth animations
- Responsive design
- Custom scrollbars
- Accessible color contrast

## Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

## Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

### Backend Connection Issues
- Verify backend is running at the configured URL
- Check CORS settings in backend
- Ensure no firewall blocking

### Build Errors
- Delete `.next` folder and `node_modules`
- Run `npm install` again
- Clear npm cache: `npm cache clean --force`

### Styling Issues
- Ensure Tailwind CSS is properly configured
- Check `globals.css` is imported in layout
- Verify PostCSS configuration

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import project in Vercel
3. Set environment variable: `NEXT_PUBLIC_API_URL` to your backend URL
4. Deploy!

### Other Platforms

Build the app:
```bash
npm run build
```

Then deploy the `.next` folder with a Node.js server.

## License

MIT
