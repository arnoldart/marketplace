# utils/db_utils.py
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database',
}

def verify_user(username, password):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        # Query untuk mendapatkan informasi pengguna berdasarkan username
        cursor.execute('SELECT id, password FROM users WHERE username = %s', (username,))
        user_data = cursor.fetchone()

        if user_data and user_data[1] == password:
            # Jika pengguna ditemukan dan password sesuai, kembalikan user_id
            return user_data[0]
    finally:
        # Tutup kursor dan koneksi database
        cursor.close()
        conn.close()

    # Jika tidak ada pengguna ditemukan atau password tidak sesuai, kembalikan None
    return None

def user_exists(username):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()

    if user_data:
        return True

    return False

def create_user(username, password):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cursor.close()
    conn.close()

def get_products():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute('SELECT id, name, image_path, price FROM products')
    products = cursor.fetchall()

    conn.close()

    return products

def get_product_by_id(product_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)  # Menggunakan dictionary cursor untuk menghasilkan hasil sebagai dictionary

    # Query untuk mendapatkan produk berdasarkan ID
    query = 'SELECT id, name, image_path, price FROM products WHERE id = %s'
    cursor.execute(query, (product_id,))
    
    product = cursor.fetchone()  # Mengambil satu baris data

    conn.close()

    return product

def add_cart(user_id, product_id, quantity):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        # Cek apakah produk sudah ada dalam keranjang
        cursor.execute('SELECT id, quantity FROM cart WHERE user_id = %s AND product_id = %s', (user_id, product_id))
        cart_item = cursor.fetchone()

        if cart_item:
            # Jika produk sudah ada dalam keranjang, update jumlahnya
            new_quantity = cart_item[1] + quantity
            cursor.execute('UPDATE cart SET quantity = %s WHERE id = %s', (new_quantity, cart_item[0]))
        else:
            # Jika produk belum ada dalam keranjang, tambahkan ke dalam keranjang
            cursor.execute('INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)',
                           (user_id, product_id, quantity))

        # Commit perubahan ke database
        conn.commit()

    finally:
        # Tutup kursor dan koneksi database
        cursor.close()
        conn.close()
        
def get_user_cart(user_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    try:
        # Query untuk mendapatkan data keranjang belanja dan informasi produk berdasarkan user_id
        cursor.execute('''
            SELECT cart.*, products.name, products.price, products.image_path
            FROM cart
            INNER JOIN products ON cart.product_id = products.id
            WHERE cart.user_id = %s
        ''', (user_id,))
        cart_data = cursor.fetchall()

        return cart_data
    finally:
        # Tutup kursor dan koneksi database
        cursor.close()
        conn.close()

def remove_item_from_cart(cart_item_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM cart WHERE id = %s', (cart_item_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
        
def clear_user_cart(user_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Gantilah 'cart' dengan nama tabel keranjang belanja Anda
        query = f"DELETE FROM cart WHERE user_id = {user_id}"

        cursor.execute(query)
        conn.commit()

    except Exception as e:
        # Tangani kesalahan jika terjadi
        print(f'Error clearing cart: {str(e)}', 'danger')

    finally:
        # Pastikan untuk selalu menutup koneksi setelah digunakan
        if conn.is_connected():
            cursor.close()
            conn.close()