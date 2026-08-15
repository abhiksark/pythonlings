def update(args):
    """Update the workspace."""
    if args.path:
        workspace_root = args.path
    else:
        workspace_root = os.getcwd()
    
    update_workspace(workspace_root)
