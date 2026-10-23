if __name__ == "__main__":
    try:
        from .main import main
        import sys
        sys.exit(main())
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Ending program")
