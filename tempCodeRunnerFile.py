  # Check if child object is a subclass of GameObject (and thus contains the update() function).
            if not issubclass(type(child), GameObject):
                return
            # Calls the update function on the child.
            child.update()