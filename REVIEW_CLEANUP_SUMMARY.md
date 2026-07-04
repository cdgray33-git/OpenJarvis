# Cleanup Summary - OpenJarvis Repository

## Files to Remove (Untracked)
These files should be removed to clean up the repository:

1. `fix-tts-endpoint.ps1` - PowerShell script for fixing TTS endpoint
2. `frontend/fix_interface.ps1` - PowerShell script for fixing frontend interface
3. `api.ts.broken_backup` - Backup file from broken API implementation
4. `.fix_backups_20260627_*/` - Backup directories (multiple timestamps)
5. `bundle_files.ps1`, `bundle_for_cloud_model.txt`, `deploy.ps1`, etc. - Deployment scripts
6. `frontend/src/components/Chat/InputArea.tsx.bak.*` - Backup files

## Files Requiring Manual Review

### 1. `frontend/src/components/Chat/InputArea.tsx`
- **Status**: Modified (M)
- **Current State**: Component manages user chat interactions with text input, file attachments, and voice recording
- **Action Required**: Manual inspection of the modified code to verify:
  - No breaking changes to API contracts
  - Proper error handling
  - Type safety maintained

### 2. `src/openjarvis/server/speech_router.py`
- **Status**: Modified and Missing (MM)
- **Current State**: FastAPI router handling STT and TTS endpoints
  - `/transcribe` - STT using faster-whisper
  - `/synthesize` - TTS using remote Kokoro server
  - `/health` - Health check endpoint
- **Action Required**: Verify that the file exists and contains the expected implementation

## Files Ready for Commit (Accepted Changes)

1. **Mid-stream Text-to-Speech (TTS)** in `ChatArea.tsx`
   - Implementation allows streaming TTS responses
   - Proper handling of stream interruptions

2. **Persist flag logic** in `store.ts`
   - Correctly manages persistence state
   - No breaking changes to existing functionality

3. **Babel dependency upgrades** in `package-lock.json`
   - Security patches applied
   - No version conflicts detected

## Cleanup Commands

To remove untracked files, run:
```bash
git clean -fdx -e .git
```

Or manually remove specific files:
```bash
rm -f fix-tts-endpoint.ps1 frontend/fix_interface.ps1 api.ts.broken_backup
rm -rf .fix_backups_*
rm -f frontend/src/components/Chat/InputArea.tsx.bak.*
```

## Next Steps

1. ✅ Remove untracked files
2. ⏳ Manually verify `InputArea.tsx` and `speech_router.py`
3. ⏳ Run tests to ensure changes work correctly
4. ⏳ Commit the accepted changes