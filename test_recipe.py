from recipe import Recipe

def test_creates_table():
    my = Recipe("test_recipe.db")
    
    my.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='history'")
    result = my.cursor.fetchone()
    
    assert result is not None
    
def test_saves_shows_history():
    my = Recipe("test_recipe.db")
    my.save_history("Pasta", "Pasta", "Italy", "Do this and that")
    
    my.cursor.execute("SELECT * FROM history WHERE recipe_name='Pasta' AND recipe_country='Italy'")
    result = my.cursor.fetchall()
    
    assert len(result) == 1
    assert result[0][1] == "Pasta"
    assert result[0][3] == "Italy"
    assert result[0][4] == "Do this and that"