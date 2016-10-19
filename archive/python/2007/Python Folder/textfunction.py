def textfunction(writing, position)
    font = pygame.font.Font(None, 36)
    text = font.render(writing, 1, (10, 10, 10))
    textpos = text.get_rect(position)
    return text, textpos
    